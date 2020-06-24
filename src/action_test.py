"""Unit tests for the action.py module."""
import os
import json
from unittest import mock

import pytest # type: ignore

from . import action, messenger


@pytest.mark.parametrize(
    "path, content",
    [
        (
            "./events/unit_test.json",
            {"commits": ["hash-0", "hash-1", "hash-2", "hash-3"]},
        )
    ],
)
def test_load_event(path, content):
    """Test loading event JSON from the on disk location."""
    result = action.load_event(path)
    assert result == content


def test_load_event_not_json():
    """Test loading not JSON from the on disk location fails correctly."""
    with pytest.raises(json.JSONDecodeError):
        action.load_event("./events/unit_test_not_json.txt")


def test_load_event_not_file():
    """Test loading from a non-file fails correctly."""
    with pytest.raises(OSError):
        action.load_event("./events/unit_test_not_a_file")


@pytest.mark.parametrize("event, commits", [({"commits": ["abc123"]}, ["abc123"])])
def test_get_commits_from_event(event, commits):
    """
    Test the get_commits_from_event method pulls commits from event objects correctly.
    """
    result = action.get_commits_from_event(event)
    assert result == commits


def test_get_commits_from_event_no_commits_key():
    """Test the get_commits_from_event fails correctly with no "commits" key."""
    with pytest.raises(KeyError):
        action.get_commits_from_event({})


@pytest.mark.parametrize(
    "commit, verified",
    [
        ({"commit": {"verification": {"verified": True}}}, True),
        ({"commit": {"verification": {"verified": False}}}, False),
    ],
)
def test_is_commit_verified(commit, verified):
    """
    Test is_commit_verified pulls the commit verification status out of the GitHub API
    response correctly.
    """
    result = action.is_commit_verified(commit)
    assert result == verified


@pytest.mark.parametrize(
    "commit", [({}), ({"commit": {}}), ({"commit": {"verification": {}}})]
)
def test_is_commit_verified_no_verified_key(commit):
    """
    Test is_commit_verified fails correctly when the verification keys are not present
    in the GitHub API repsonse object.
    """
    with pytest.raises(KeyError):
        action.is_commit_verified(commit)


@mock.patch("src.action.github")
def test_get_unverified_commits(github):
    """
    Test get_unverified_commits calls the GitHub API client correctly for each supplied
    commit hash.
    """
    token = "test-github-token"
    repo = "github/repo-name"
    hashes = ["hash-1", "hash-2", "hash-3", "hash-4"]
    expected = [
        {"commit": {"id": "hash-2", "verification": {"verified": False}}},
        {"commit": {"id": "hash-4", "verification": {"verified": False}}},
    ]

    github.GitHubApiClient.return_value.get_commit.side_effect = [
        {"commit": {"id": "hash-1", "verification": {"verified": True}}},
        {"commit": {"id": "hash-2", "verification": {"verified": False}}},
        {"commit": {"id": "hash-3", "verification": {"verified": True}}},
        {"commit": {"id": "hash-4", "verification": {"verified": False}}},
    ]

    result = action.get_unverified_commits(token=token, repo=repo, commit_hashes=hashes)
    assert result == expected
    github.GitHubApiClient.assert_called_once_with(token)


def test_group_by_author():
    """
    Test group_by_author groups a list of commit objects from the GitHub API correclty.
    """
    commits = [
        {"id": 1, "author": {"login": "user1"}},
        {"id": 2, "author": {"login": "user1"}},
        {"id": 3, "author": {"login": "user2"}},
        {"id": 4, "author": {"login": "user2"}},
        {"id": 5, "author": {"login": "user2"}},
    ]

    expected = {
        "user1": [
            {"id": 1, "author": {"login": "user1"}},
            {"id": 2, "author": {"login": "user1"}},
        ],
        "user2": [
            {"id": 3, "author": {"login": "user2"}},
            {"id": 4, "author": {"login": "user2"}},
            {"id": 5, "author": {"login": "user2"}},
        ],
    }

    result = action.group_by_author(commits)
    assert result == expected


@pytest.mark.parametrize("commits", [[{}], [{"author": {}}]])
def test_group_by_author_no_author_key(commits):
    """
    Test group_by_author fails correclty when the author keys are not present in the
    GitHub API response object.
    """
    with pytest.raises(KeyError):
        action.group_by_author(commits)


@pytest.mark.parametrize("env_name, func", [("console", messenger.send_to_console)])
def test_select_backend(env_name, func):
    """
    Test select_backend correctly selects the backend messenger from the
    `MESSAGE_BACKEND` env var.
    """
    os.environ["MESSAGE_BACKEND"] = env_name
    result = action.select_backend()
    assert result == func  # pylint: disable=comparison-with-callable


def test_select_backend_unknown():
    """
    Test select_backend fails correclty when the `MESSAGE_BACKEND` env var is invalid.
    """
    os.environ["MESSAGE_BACKEND"] = "unknown_env_name"
    with pytest.raises(ValueError):
        action.select_backend()


@mock.patch("src.action.messenger")
def test_send_messages(messenger):  # pylint: disable=redefined-outer-name
    """Test send_messages correctly calls a configured messenger backend."""
    os.environ["MESSAGE_BACKEND"] = "console"
    repo = "github/repo-name"
    grouped_commits = {
        "user1": [
            {"id": 1, "author": {"login": "user1"}},
            {"id": 2, "author": {"login": "user1"}},
        ],
        "user2": [
            {"id": 3, "author": {"login": "user2"}},
            {"id": 4, "author": {"login": "user2"}},
            {"id": 5, "author": {"login": "user2"}},
        ],
    }

    action.send_messages(repo, grouped_commits)

    messenger.send_to_console.assert_any_call(
        author="user1", repo=repo, commits=grouped_commits["user1"]
    )
    messenger.send_to_console.assert_any_call(
        author="user2", repo=repo, commits=grouped_commits["user2"]
    )


@mock.patch("src.action.github")
def test_main(github):
    """Test the action end-to-end to see everything working together correctly."""
    os.environ["GITHUB_REPOSITORY"] = "github/repo-name"
    os.environ["GITHUB_EVENT_PATH"] = "./events/unit_test.json"
    os.environ["GITHUB_TOKEN"] = "github-test-token"

    def mock_get_commit(repo, sha):
        assert repo == "github/repo-name"
        if sha == "hash-1":
            return {
                "author": {"login": "user1"},
                "commit": {"verification": {"verified": False}},
                "url": f"https://github.com/{repo}/commit/{sha}",
            }
        return {
            "author": {"login": "user1"},
            "commit": {"verification": {"verified": True}},
            "url": f"https://github.com/{repo}/commit/{sha}",
        }

    github.GitHubApiClient.return_value.get_commit = mock_get_commit

    commit_count = action.main()
    assert commit_count == 1
    github.GitHubApiClient.assert_called_once_with("github-test-token")
