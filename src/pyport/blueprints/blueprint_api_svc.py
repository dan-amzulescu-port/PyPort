from typing import Dict, List


class Blueprints:
    def __init__(self, client):
        self._client = client

    def get_blueprints(self) -> List[Dict]:
        """Get all blueprints"""
        response = self._client.make_request('GET', 'blueprints')
        return response.json()
