from injector import inject
from dataclasses import dataclass
from typing import Dict

from helper import Config
from model.cluster import Cluster
from model.enforcement import make_default_enforcement
from data import EnforcementRepository


@inject
@dataclass
class ClusterFactory:
    _config: Config
    _enforcement_repository: EnforcementRepository

    def create(self, cluster_map: Dict[str, str]) -> Cluster:
        cluster_name = cluster_map['name']
        return Cluster(
            url=self._make_cluster_url(cluster_map),
            token=self._config.rancher_token,
            id=cluster_map.get('id'),
            name=cluster_name,
            _enforcement_repository=self._enforcement_repository,
            _default_enforcement_factory=make_default_enforcement(cluster_name, self._config)
        )

    def _make_cluster_url(self, cluster_map: Dict[str, str]) -> str:
        if cluster_map.get('url') is None:
            return f"{self._config.rancher_url}/k8s/clusters/{cluster_map['id']}"
        else:
            return cluster_map.get('url', '')


