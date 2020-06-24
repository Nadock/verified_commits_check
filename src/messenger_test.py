"""Unit tests for the messenger.py module."""
from . import messenger


def test_console_fmt():
    """Test the console formatter formats output correclty."""
    # pylint: disable=protected-access
    author = "test-user"
    repo = "github/repo-name"
    commits = [{"url": "https://url.1"}, {"url": "https://url.2"}]

    expected = (
        f"GitHub User {author} pushed the following {len(commits)} unverified commits "
        f"to {repo}:\n\n\t* {commits[0]['url']}\n\t* {commits[1]['url']}\n"
    )

    result = messenger._console_fmt(author=author, repo=repo, commits=commits)
    assert result == expected
