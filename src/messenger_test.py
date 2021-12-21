"""Unit tests for the messenger.py module."""
from unittest import mock
import os
from . import messenger


def test_send_to_console(capsys):
    """Test send_to_console formats output correclty."""
    # pylint: disable=protected-access
    author = "test-user"
    repo = "github/repo-name"
    commits = [{"html_url": "https://url.1"}, {"html_url": "https://url.2"}]

    expected = (
        "GitHub user Test-User pushed 2 unverified commits to github/repo-name:"
        "\n\n\t* https://url.1\n\t* https://url.2\n"
    )

    messenger.send_to_console(author=author, repo=repo, commits=commits)

    captured = capsys.readouterr()
    assert captured.out == expected


@mock.patch("src.messenger.requests")
def test_send_to_slack(requests):
    """
    Test send_to_slack formats a message and POSTs it to the webhook URL correclty.
    """
    author = "test-user"
    repo = "github/repo-name"
    commits = [
        {"html_url": "https://url.1", "sha": "sha1"},
        {"html_url": "https://url.2", "sha": "sha2"},
    ]
    url = "https://google.com"
    os.environ["SLACK_WEBHOOK_URL"] = url

    messenger.send_to_slack(author=author, repo=repo, commits=commits)

    text = "Test-User pushed 2 unverified commits"
    markdown = (
        "GitHub user `<https://github.com/test-user|Test-User>` pushed *2* unverified "
        "commits to `<https://github.com/github/repo-name|github/repo-name>`\n"
        "\t:heavy_minus_sign: `<https://url.1|sha1>`\n"
        "\t:heavy_minus_sign: `<https://url.2|sha2>`\n"
    )

    expected = {
        "text": text,
        "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": markdown}}],
    }

    requests.post.return_value.raise_for_status.assert_called_once()
    requests.post.assert_called_once_with(url, json=expected)
