from dataclasses import dataclass
from typing import List, Dict

from injector import inject

from app.data.repository import ClusterRepository
from app.helper.config import Config
from app.model.entities import Cluster


@inject
@dataclass
class ClusterMonitor:
    _cluster_repository: ClusterRepository
    _config: Config

    def detect_new_clusters(self, rancher_clusters: List[Cluster]) -> List[Cluster]:
        argo_clusters_info = self._cluster_repository.list_clusters_info()
        cluster_info_names = {cluster['name'] for cluster in argo_clusters_info}

        return list(
                    filter(
                        lambda cluster: cluster.name not in cluster_info_names,
                        rancher_clusters
                    )
        )

    def detect_deleted_clusters(self, rancher_clusters: List[Cluster]) -> List[Cluster]:

        clusters_map: Dict[str, Cluster] = {cluster.name: cluster for cluster in rancher_clusters}
        argo_clusters_info = self._cluster_repository.list_clusters_info()

        return list(
                    map(
                        lambda info: clusters_map[info['name']],
                        filter(
                            lambda info: info['name'] not in clusters_map,
                            argo_clusters_info
                        )
                    )
        )

    def register(self, cluster: Cluster) -> None:
        self._cluster_repository.register_cluster(cluster)

    def unregister(self, cluster: Cluster) -> None:
        if cluster.name != 'in-cluster':
            self._cluster_repository.unregister_cluster(cluster)

