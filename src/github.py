"""API interactions with GitHub."""
import logging
import os
from urllib import parse
from typing import Dict, Optional

import requests

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(os.environ.get("LOG_LEVEL", "INFO"))


class GitHubApiClient:
    """API Client for interacting with GitHub's v3 REST API."""

    base_url = "https://api.github.com"

    def __init__(self, token):
        self.token = token
        if not self.token:
            raise ValueError("GitHub token value must not be None or empty")

    def headers(self, extra: Optional[Dict[str, str]]) -> Dict[str, str]:
        """
        Generate a dict of headers to include in each request.

        `extra` headers will be combined with the default headers, overwriting on
        duplicate keys.
        """
        if not extra:
            extra = {}

        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.token}",
        }

        return {**headers, **extra}

    def get(
        self,
        endpoint: str,
        *,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Optional[dict]:
        """Perform a HTTP GET request and unwrap the response."""
        headers = self.headers(headers)
        url = parse.urljoin(self.base_url, endpoint)

        resp = requests.get(url, params=params, headers=headers)
        return unwrap_requests_response(resp)

    def get_commit(self, *, repo: str, sha: str) -> dict:
        """Get the details of a specified git commit."""
        endpoint = f"/repos/{repo}/commits/{sha}"
        resp = self.get(endpoint)
        if not resp:
            raise ValueError(f"Invalid empty response from GitHub API {endpoint}")
        return resp


def unwrap_requests_response(response: requests.Response) -> Optional[dict]:
    """
    Get JSON body from a `requests.Response` and check the response status code is in
    [200, 300).
    """
    body = None
    if response.content:
        try:
            body = response.json()
        except Exception as ex:
            LOGGER.error(f"Error reading JSON from response body: {ex}")
            raise ex

    try:
        response.raise_for_status()
    except Exception as ex:
        LOGGER.error(f"GitHub API error: {ex}")
        LOGGER.debug(f"GitHub API response body: {body}")
        raise ex

    return body
