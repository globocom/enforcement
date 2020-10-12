from dataclasses import dataclass
from typing import List

import requests
from injector import inject

from helper.config import Config
from data.datasource.datasource import ClusterDatasource
from model.cluster import Cluster


@inject
@dataclass
class RancherRepository(ClusterDatasource):
    _config: Config

    def get_clusters(self, **params: dict) -> List[Cluster]:
        headers = {
            "Authorization": f"Bearer {self._config.rancher_token}"
        }

        filters: dict = params.get('filters') if params.get('filters') else dict()
        filters.update({'state': 'active'})

        url = f"{self._config.rancher_url}/v3/clusters"

        with requests.get(
            url, verify=False, headers=headers, params=filters,
        ) as response:
            response.raise_for_status()
            return self._build_clusters(response.json()['data'])

    def _build_clusters(self, cluster_map_list: dict) -> List[Cluster]:
        clusters: List[Cluster] = []
        for cluster in cluster_map_list:
            clusters.append(
                Cluster(
                    name=cluster['name'],
                    id=cluster['id'],
                    token=self._config.rancher_token,
                    url=f'{self._config.rancher_url}/k8s/clusters/{cluster["id"]}',
                )
            )
        return clusters



