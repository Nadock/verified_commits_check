"""Unit tests for the github.py module."""
import json
from unittest import mock

import pytest  # type: ignore

from . import github


def test_unwrap_requests_response_no_body_okay():
    """Test unwrap_requests_response with no body but okay status code."""
    mock_resp = mock.MagicMock()
    mock_resp.content = None

    result = github.unwrap_requests_response(mock_resp)
    assert result is None


def test_unwrap_requests_response_no_body_not_okay():
    """Test unwrap_requests_response with no body and not okay status code."""
    mock_resp = mock.MagicMock()
    mock_resp.content = None
    mock_resp.raise_for_status.side_effect = Exception

    with pytest.raises(Exception):
        github.unwrap_requests_response(mock_resp)


def test_unwrap_requests_response_body_okay():
    """Test unwrap_requests_response with body and okay status code."""
    mock_resp = mock.MagicMock()
    mock_resp.content = '{"key":"value"}'
    mock_resp.json.return_value = json.loads(mock_resp.content)

    result = github.unwrap_requests_response(mock_resp)
    assert result == json.loads(mock_resp.content)


def test_unwrap_requests_response_body_not_okay():
    """Test unwrap_requests_response with body but not okay status code."""
    mock_resp = mock.MagicMock()
    mock_resp.content = '{"key":"value"}'
    mock_resp.json.return_value = json.loads(mock_resp.content)
    mock_resp.raise_for_status.side_effect = Exception

    with pytest.raises(Exception):
        github.unwrap_requests_response(mock_resp)


@pytest.mark.parametrize(
    "extra", [None, {}, {"key": "value"}, {"Accept": "application/json"}]
)
def test_github_api_client_headers(extra):
    """
    Test `GitHubApiClient.headers` method correctly generates default headers and merges
    supplied extra headers.
    """
    client = github.GitHubApiClient("github-test-token")
    headers = client.headers(extra)
    assert headers

    if extra:
        for k, v in extra.items():  # pylint: disable=invalid-name
            assert headers[k] == v
    if not extra or "Accept" not in extra.keys():
        assert headers["Accept"] == "application/vnd.github.v3+json"
    if not extra or "Authorization" not in extra.keys():
        assert headers["Authorization"] == "token github-test-token"


@mock.patch("src.github.requests")
def test_github_api_client_get(requests):
    """
    Test `GitHubApiClient.get` method correctly builds headers and the API URL, then
    calls `requests.get` to do a HTTP GET call to the GitHub API.
    """
    endpoint = "/api/endpoint"
    params = {"key": "value"}
    headers = {"X-custom-header": "hello"}

    client = github.GitHubApiClient("github-test-token")
    client.get(endpoint, params=params, headers=headers)

    expected_headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": "token github-test-token",
        "X-custom-header": "hello",
    }

    requests.get.assert_called_once_with(
        "https://api.github.com/api/endpoint", params=params, headers=expected_headers
    )


@mock.patch("src.github.requests")
def test_github_api_client_get_commit(requests):
    """
    Test `GitHubApiClient.get_commits` correctly builds the API endpoint and triggers
    the HTTP GET call via `requests.get`.
    """
    repo = "github/repo-name"
    sha = "hash-1"

    client = github.GitHubApiClient("github-test-token")
    result = client.get_commit(repo=repo, sha=sha)

    assert result == requests.get.return_value.json.return_value

    requests.get.assert_called_once_with(
        f"https://api.github.com/repos/{repo}/commits/{sha}",
        params=None,
        headers=mock.ANY,
    )


@mock.patch("src.github.requests")
def test_github_api_client_get_commit_bad_resp(requests):
    """
    Test `GitHubApiClient.get_commits` correctly raises a `ValueError` if the GitHub
    API does not send back any data.
    """
    repo = "github/repo-name"
    sha = "hash-1"

    requests.get.return_value.content = None

    client = github.GitHubApiClient("github-test-token")
    with pytest.raises(ValueError):
        client.get_commit(repo=repo, sha=sha)

    requests.get.assert_called_once_with(
        f"https://api.github.com/repos/{repo}/commits/{sha}",
        params=None,
        headers=mock.ANY,
    )
