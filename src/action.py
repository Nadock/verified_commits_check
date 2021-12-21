"""
Verified Commtis Check GitHub Action.

When run as a GitHub Action on every push to a repository, it can detect and check
whenever a user pushes unverified commits to GitHub.
"""
import json
import logging
import os
import sys
from typing import Dict, List

from . import github, messenger

LOGGER = logging.getLogger("verified_commits_check")


def main():
    """Run the verified commits check and check on any unverified commits."""
    try:
        github_repository = os.environ["GITHUB_REPOSITORY"]
        github_event_path = os.environ["GITHUB_EVENT_PATH"]
        github_event_name = os.environ["GITHUB_EVENT_NAME"]
        github_token = os.environ["GITHUB_TOKEN"]
    except KeyError as ex:
        LOGGER.error(f"Environment variable {ex} must be set")
        raise ex

    if github_event_name != "push":
        LOGGER.error(
            f"This action only supports push type events, not {github_event_name}"
        )
        return 1

    event = load_event(github_event_path)
    LOGGER.debug(f"Loaded event from {github_event_path}")

    commit_hashes = get_commits_from_event(event)
    LOGGER.debug(f"Event contained these hashes: {commit_hashes}")

    commits = get_unverified_commits(
        token=github_token, repo=github_repository, commit_hashes=commit_hashes
    )
    LOGGER.debug(f"The following commits are unverified: {commits}")

    grouped_commits = group_by_author(commits)
    LOGGER.debug(f"Commits grouped by their author: {grouped_commits}")

    send_messages(github_repository, grouped_commits)

    return len(commits)


def send_messages(repo: str, grouped_commits: Dict[str, dict]):
    """Send messages for the unverified commits."""
    backend = select_backend()
    LOGGER.debug(f"Selected messenger backed: {backend}")

    for author, commits in grouped_commits.items():
        backend(author=author, repo=repo, commits=commits)


def select_backend():
    """
    Select the messaging backend function based on the `MESSAGE_BACKEND` environment
    variable.
    """
    message_backend = os.environ.get("MESSAGE_BACKEND", "console").lower()
    if message_backend == "console":
        return messenger.send_to_console
    if message_backend == "slack":
        return messenger.send_to_slack

    raise ValueError(f"Unknown message backend {message_backend}")


def group_by_author(commits: List[dict]) -> Dict[str, List[dict]]:
    """Group GitHub commit objects by their author."""
    grouped: Dict[str, List[dict]] = {}
    for commit in commits:
        name = commit["author"]["login"]
        if name not in grouped:
            grouped[name] = []
        grouped[name].append(commit)
    return grouped


def get_unverified_commits(
    *, token: str, repo: str, commit_hashes: List[str]
) -> List[dict]:
    """
    Get a subset commit_hashes that refer to unverified commits.

    `token` should be a OAuth token to authenticate to GitHub.

    `repo` should be the name of the GitHub repo to which the commits refer, in
    `{owner}/{repo}` format.

    `commit_hashes` should be a list of git hashes to check the verification status of.
    """
    github_client = github.GitHubApiClient(token)
    commits = []

    for sha in commit_hashes:
        commit = github_client.get_commit(repo=repo, sha=sha)
        if not is_commit_verified(commit):
            commits.append(commit)

    return commits


def is_commit_verified(commit: dict) -> bool:
    """`True` if a Github commit is verified, `False` otherwise."""
    return commit["commit"]["verification"]["verified"]


def get_commits_from_event(event: dict) -> List[str]:
    """Get a list of commit hashes from a GitHub push event object."""
    return [commit["id"] for commit in event["commits"]]


def load_event(path: str) -> dict:
    """Load a GitHub event from a JSON file stored on disk at `path`."""
    with open(path, encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":
    # Configure root logger formatting
    logging_handler = logging.StreamHandler()
    logging_handler.setLevel(os.environ.get("LOG_LEVEL", "INFO").upper())
    logging_handler.setFormatter(
        logging.Formatter("[%(levelname)s %(name)s %(lineno)d] %(message)s")
    )

    logger = logging.getLogger()
    logger.addHandler(logging_handler)

    sys.exit(main())
