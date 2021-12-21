"""
Format and send a message indicating the git commits listed in hashes are not verified.

Each sender method should have the same signature as `send_to_console`.
"""
import logging
import os
from typing import List

import requests

LOGGER = logging.getLogger(__name__)


def send_to_console(*, author: str, repo: str, commits: List[dict]):
    """
    Print a message to std::out describing the unverified commits.

    `send_to_console` is the demonstration send method, the parameters have the same
    meaning in all other send methods.

    `author` the name of the GitHub user who authored the `commits`.

    `repo` is the name of the GitHub repo these commits can be found in, in
    `{owner}/{name}` format.

    `commits` is the list of commits that were unverified.
    """
    msg = (
        f"GitHub user {author.title()} pushed {len(commits)} "
        f"unverified commits to {repo}:\n\n"
    )
    msg += "\n".join([f"\t* {commit['html_url']}" for commit in commits])

    print(msg)


def send_to_slack(*, author: str, repo: str, commits: List[dict]):
    """
    Send a message to a Slack webhook URL describing the unverified commits.

    Formats both a plaintext and markdown message and sends it to the Slack webhook URL
    in the environment variable `SLACK_WEBHOOK_URL`.

    Arguments are the same as in `send_to_console`.
    """
    markdown = (
        f"GitHub user `<https://github.com/{author}|{author.title()}>` pushed "
        f"*{len(commits)}* unverified commits to `<https://github.com/{repo}|{repo}>`\n"
    )
    for commit in commits:
        markdown += f"\t:heavy_minus_sign: `<{commit['html_url']}|{commit['sha']}>`\n"

    # Simplified plaintext message for notification body and anywhere else that can't
    # display the entire markdown message
    plain_text = f"{author.title()} pushed {len(commits)} unverified commits"

    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    body = {
        "text": plain_text,
        "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": markdown}}],
    }

    try:
        LOGGER.debug(f"POST {webhook_url} {body}")
        resp = requests.post(webhook_url, json=body)
        resp.raise_for_status()
    except Exception:
        LOGGER.error(f"Unable to publish to Slack webhook: {resp.text}")
        raise
