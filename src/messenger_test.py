"""Unit tests for the messenger.py module."""
from . import messenger


def test_send_to_console(capsys):
    """Test send_to_console formats output correclty."""
    # pylint: disable=protected-access
    author = "test-user"
    repo = "github/repo-name"
    commits = [{"url": "https://url.1"}, {"url": "https://url.2"}]

    expected = (
        f"GitHub User {author} pushed the following {len(commits)} unverified commits "
        f"to {repo}:\n\n\t* {commits[0]['url']}\n\t* {commits[1]['url']}\n"
    )

    messenger.send_to_console(author=author, repo=repo, commits=commits)

    captured = capsys.readouterr()
    assert captured.out == expected
