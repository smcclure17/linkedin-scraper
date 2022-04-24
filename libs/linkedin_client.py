from typing import Any, Dict
import requests

import logging
logging.basicConfig(level=logging.INFO)  # Display all logs

# With heavy inspiration from https://github.com/tomquirk/linkedin-api
class LinkedInClient:
    """Client to wrap a requests session for use in querying LinkedIn data."""

    session: requests.Session

    AUTH_REQUEST_HEADERS = {
        "X-Li-User-Agent": "LIAuthLibrary:3.2.4 com.linkedin.LinkedIn:8.8.1 iPhone:8.3",
    }

    REQUEST_HEADERS = {
        "user-agent": " ".join(
            [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5)",
                "AppleWebKit/537.36 (KHTML, like Gecko)",
                "Chrome/83.0.4103.116 Safari/537.36",
            ]
        )
    }

    def __init__(self):
        self.session = requests.Session()
        cookies = self._get_auth_cookies()
        self._set_cookies(cookies=cookies)

    @classmethod
    def from_user(self, username: str, password: str) -> "LinkedInClient":
        """Method for initializing and authorizing a client with a user's credentials.

        Please be smart (e.g. use environment variables) when storing/using your
        LinkedIn credentials--I don't want to have ur info or see it leaked :(

        params:
            user: LinkedIn account email address
            password: LinkedIn account password
        """
        client = LinkedInClient()
        client.authenticate(user=username, password=password)
        return client

    def _set_cookies(self, cookies: Dict[str, Any]):
        self.session.cookies = cookies
        self.session.headers["csrf-token"] = self.session.cookies["JSESSIONID"].strip(
            '"'
        )

    def authenticate(self, user: str, password: str):
        data = {
            "session_key": user,
            "session_password": password,
            "JSESSIONID": self.session.cookies["JSESSIONID"],
        }

        res = requests.post(
            "https://www.linkedin.com/uas/authenticate",
            data=data,
            cookies=self.session.cookies,
            headers=self.AUTH_REQUEST_HEADERS,
        )

        logging.info(f"authenticated user with status code {res.status_code}")
        res.raise_for_status()
        self._set_cookies(res.cookies)

    def _get_auth_cookies(self):
        return requests.get(
            "https://www.linkedin.com/uas/authenticate",
            headers=self.AUTH_REQUEST_HEADERS,
        ).cookies
