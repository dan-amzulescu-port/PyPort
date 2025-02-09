import os
import unittest
from unittest.mock import patch, MagicMock

# Import the PortClient from your source code.
from pyport.api_client import PortClient


class TestPortClient(unittest.TestCase):
    @patch('pyport.api_client.requests.post')
    def test_get_access_token(self, mock_post):
        # Setup: Create a fake token response.
        expected_token = 'testtoken123'
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'accessToken': expected_token}
        mock_post.return_value = mock_response

        # Optionally, set the environment variables if not passing credentials.
        os.environ['PORT_CLIENT_ID'] = 'dummy'
        os.environ['PORT_CLIENT_SECRET'] = 'dummy'

        # Create the PortClient. Disable auto-refresh for testing.
        client = PortClient(auto_refresh=False)

        # Assert that the client token matches the fake token.
        self.assertEqual(client.token, expected_token)

    @patch('pyport.api_client.requests.Session.request')
    def test_make_request(self, mock_request):
        # Setup: Prepare a mock response for a generic API call.
        expected_json = {"key": "value"}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_json
        mock_request.return_value = mock_response

        # Create the PortClient with auto-refresh disabled.
        client = PortClient(auto_refresh=False)

        # Make a sample GET request.
        response = client.make_request('GET', 'test-endpoint')

        # Assert that the response contains the expected JSON.
        self.assertEqual(response.json(), expected_json)


if __name__ == '__main__':
    unittest.main()
