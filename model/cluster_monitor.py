from dataclasses import dataclass
from typing import List, Callable, Dict

from injector import inject

from data import RancherRepository, ClusterRepository
from helper import Config
from model.cluster import Cluster
from model.cluster_factory import ClusterFactory


@inject
@dataclass
class ClusterMonitor:
    _rancher_repository: RancherRepository
    _cluster_repository: ClusterRepository
    _cluster_factory: ClusterFactory
    _config: Config

    def detect_new_clusters(self) -> List[Cluster]:
        self._load()
        cluster_info_names = {cluster['name'] for cluster in self._argo_clusters_info}
        evaluated_clusters = cluster_info_names.union(self._config.ignore_clusters)

        return self.__filter_and_create_cluster_instances(
            lambda cluster: cluster['name'] not in evaluated_clusters,
            self._rancher_clusters,
        )

    def detect_deleted_clusters(self) -> List[Cluster]:
        self._load()
        clusters_map = {cluster['name']: cluster for cluster in self._rancher_clusters}

        return self.__filter_and_create_cluster_instances(
            lambda cluster_info: cluster_info["name"] not in clusters_map,
            self._argo_clusters_info,
        )

    def __filter_and_create_cluster_instances(
        self,
        filter_function: Callable[[Dict[str, str]], bool],
        raw_cluster_list: List[Dict[str, str]],
    ) -> List[Cluster]:
        return [
            self._cluster_factory.create(cluster)
            for cluster in raw_cluster_list if filter_function(cluster)
        ]

    def register(self, cluster: Cluster) -> None:
        self._cluster_repository.register_cluster(cluster)

    def unregister(self, cluster: Cluster) -> None:
        if cluster.name != 'in-cluster':
            self._cluster_repository.unregister_cluster(cluster)

    def _load(self) -> None:
        self._rancher_clusters = self._rancher_repository.get_clusters(state="active")
        self._argo_clusters_info = self._cluster_repository.list_clusters_info()
