from typing import List
import requests

from data.datasource.datasource import ClusterDatasource
from model.entities import RancherSource
from model.cluster import Cluster


class RancherDatasource(ClusterDatasource):

    def get_clusters(self, source: RancherSource) -> List[Cluster]:
        headers = {
            "Authorization": f"Bearer {self._config.rancher_token}"
        }

        filters: dict = source.filters if source.filters else dict()
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



