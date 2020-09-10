from injector import inject
from helper.config import Config
import requests

from dataclasses import dataclass


@inject
@dataclass
class RancherService:
    _config: Config

    def get_clusters(self) -> str:
        headers = {
            "Authorization": f"Bearer {self._config.rancher_token}"
        }
        url = f"{self._config.rancher_url}/clusters"
        response = requests.get(url, verify=False, headers=headers)

        try:
            response.raise_for_status()
        finally:
            response.close()

        return response.json()['data']

