import os
import unittest
from unittest.mock import patch, MagicMock

# Import the PortClient from your local package.
from src.pyport.api_client import PortClient


class TestPortClientInitialization(unittest.TestCase):
    @patch('src.pyport.api_client.PortClient._get_access_token', return_value='dummy_token')
    def test_initialization(self, mock_get_token):
        """
        Test that the PortClient is initialized correctly and that
        _get_access_token is patched to return a dummy token.
        """
        client = PortClient(auto_refresh=False)
        # Check that the token is set to the dummy value.
        self.assertEqual(client.token, 'dummy_token')
        # Verify that the session headers are updated with the dummy token.
        self.assertEqual(client._session.headers.get("Authorization"), "Bearer dummy_token")

    @patch('src.pyport.api_client.PortClient._get_access_token', return_value='dummy_token')
    @patch('src.pyport.api_client.requests.Session.request')
    def test_make_request(self, mock_request, mock_get_token):
        """
        Test the make_request method using a patched _get_access_token.
        """
        expected_json = {"key": "value"}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_json
        mock_request.return_value = mock_response

        client = PortClient(auto_refresh=False)
        response = client.make_request('GET', 'test-endpoint')
        self.assertEqual(response.json(), expected_json)


if __name__ == '__main__':
    unittest.main()
