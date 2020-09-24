from injector import inject
from helper.config import Config
import requests
from typing import List

from dataclasses import dataclass


@inject
@dataclass
class RancherRepository:
    _config: Config

    def get_clusters(self, **filters) -> List[dict]:
        headers = {
            "Authorization": f"Bearer {self._config.rancher_token}"
        }
        url = f"{self._config.rancher_url}/v3/clusters"
        response = requests.get(url, verify=False, headers=headers, params=filters)

        try:
            response.raise_for_status()
        finally:
            response.close()

        return response.json()['data']

