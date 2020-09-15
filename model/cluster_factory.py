from injector import inject
from dataclasses import dataclass

from helper import Config
from model.cluster import Cluster


@inject
@dataclass
class ClusterFactory:
    _config: Config

    def create(self, cluster_map):
        return Cluster(
            url=self._make_cluster_url(cluster_map),
            token=self._config.rancher_token,
            id=cluster_map.get('id'),
            name=cluster_map.get('name')
        )

    def _make_cluster_url(self, cluster_map) -> str:
        if cluster_map.get('url') is None:
            return f"{self._config.rancher_url}/k8s/clusters/{cluster_map['id']}"
        else:
            return cluster_map.get('url')


