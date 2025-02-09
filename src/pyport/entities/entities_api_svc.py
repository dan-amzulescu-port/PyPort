import json
import requests
import logging

from package import PortClient
from pyport.services.port_api_svc import get_requests_headers

logger = logging.getLogger(__name__)


def update_port_blueprint(pc: PortClient, blueprint: str, list_of_entities: list[dict]) -> None:
    headers = get_requests_headers(pc.token)
    url = f"{pc.api_url}/blueprints/{blueprint}/entities"

    for entity in list_of_entities:
        payload = json.dumps(entity)
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 201:
            logger.error(f"Rest API response of creating entities was not 200: {response.status_code}")
