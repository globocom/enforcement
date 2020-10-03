from dataclasses import dataclass
from typing import Dict, List, Any

import requests
from injector import inject

from helper.config import Config


@inject
@dataclass
class RancherRepository:
    _config: Config

    def get_clusters(self, **filters: Any) -> List[Dict[str, str]]:
        headers = {
            "Authorization": f"Bearer {self._config.rancher_token}"
        }
        url = f"{self._config.rancher_url}/v3/clusters"
        response = requests.get(url, verify=False, headers=headers, params=filters)

        try:
            response.raise_for_status()
        finally:
            response.close()

        return response.json()['data']  # type: ignore[no-any-return]

