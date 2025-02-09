import json
import logging
import os

import requests

from src.constants import PORT_API_US_URL, PORT_API_URL, GENERIC_HEADERS
from pyport.blueprints.blueprint_api_svc import Blueprints


class PortClient:
    def __init__(self, client_id: str = "", client_secret: str = "", us_region: bool = False):
        self.api_url = PORT_API_US_URL if us_region else PORT_API_URL

        self._logger = logging.getLogger(__name__)
        self.token = self._get_access_token(client_id, client_secret)

        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        })
        # Initialize sub-clients
        self.blueprints = Blueprints(self)

    def _get_access_token(self, client_id: str = "", client_secret: str = "") -> str:
        try:
            headers = GENERIC_HEADERS

            if not client_id or not client_secret:
                client_id, client_secret = self._get_local_env_cred()

            credentials = {'clientId': client_id, 'clientSecret': client_secret}
            payload = json.dumps(credentials)
            self._logger.debug("Sending authentication request to obtain access token...")

            token_response = requests.post(f'{self.api_url}/auth/access_token', headers=headers, data=payload)

            if token_response.status_code != 200:
                self._logger.error(
                    f"Failed to obtain access token. Status code: {token_response.status_code}. "
                    f"Response: {token_response.text}")
                token_response.raise_for_status()  # Raise an HTTP error if the response code is not 200

            token = token_response.json().get('accessToken')
            if not token:
                self._logger.error("Access token not found in the response.")
                raise ValueError("Access token not present in the API response.")

            return token

        except Exception as e:
            self._logger.error(f"An unexpected error occurred: {str(e)}")
            raise

    def _get_local_env_cred(self):
        # Get environment variables
        PORT_CLIENT_ID = os.getenv("PORT_CLIENT_ID")
        PORT_CLIENT_SECRET = os.getenv("PORT_CLIENT_SECRET")
        # Ensure the required environment variables are provided
        if not PORT_CLIENT_ID or not PORT_CLIENT_SECRET:
            self._logger.error("Missing environment variables: PORT_CLIENT_ID or PORT_CLIENT_SECRET.")
            raise ValueError("Environment variables PORT_CLIENT_ID or PORT_CLIENT_SECRET are not set")
        return PORT_CLIENT_ID, PORT_CLIENT_SECRET

    def make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Make an HTTP request to the API
        """
        url = f"{self.api_url}/{endpoint}"
        response = self._session.request(method, url, **kwargs)
        response.raise_for_status()
        return response
