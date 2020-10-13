from typing import List, Dict
import requests

from data.datasource.datasource import ClusterDatasource
from model.entities import Cluster, EnforcementSource


class RancherDatasource(ClusterDatasource):

    def get_clusters(self, source: EnforcementSource) -> List[Cluster]:
        headers = {
            "Authorization": f"Bearer {self._config.rancher_token}"
        }

        filters: dict = source.rancher.filters if source.rancher.filters else dict()
        filters.update({'state': 'active'})

        url = f"{self._config.rancher_url}/v3/clusters"

        with requests.get(
            url, verify=False, headers=headers, params=filters,
        ) as response:
            response.raise_for_status()
            return self._filter_and_map_clusters(
                response.json()['data'], source.rancher.labels, source.rancher.ignore
            )

    def _filter_and_map_clusters(self, clusters_list: List[Dict], labels: dict, ignore: List[str]) -> List[Cluster]:
        return list(
                    map(
                        self._build_cluster,
                        filter(
                            lambda cluster_map: self._filter_cluster(cluster_map, labels, ignore),
                            clusters_list
                        )
                    )
        )

    def _filter_cluster(self, cluster_map: dict, labels: dict, ignore: List[str]) -> bool:
        if ignore and cluster_map['name'] in ignore:
            return False

        return set(labels.items()).issubset(set(cluster_map['labels'].items())) if labels else True

    def _build_cluster(self, cluster_map: dict) -> Cluster:
        return Cluster(
            name=cluster_map['name'],
            id=cluster_map['id'],
            token=self._config.rancher_token,
            url=f'{self._config.rancher_url}/k8s/clusters/{cluster_map["id"]}',
        )



