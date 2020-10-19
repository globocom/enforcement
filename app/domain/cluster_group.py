from typing import List, Dict
import attr

from app.domain.entities import Cluster
from app.domain.repositories import ClusterRepository


@attr.s(auto_attribs=True)
class ClusterGroup:
    _clusters: List[Cluster]
    _cluster_repository: ClusterRepository

    @property
    def clusters(self):
        return self._clusters

    def register(self):
        for cluster in self._clusters:
            self._cluster_repository.register_cluster(cluster)

    def unregister(self):
        for cluster in self._clusters:
            self._cluster_repository.unregister_cluster(cluster)

    def detect_new_clusters(self) -> List[Cluster]:
        monitored_clusters_info = self._cluster_repository.list_clusters_info()
        monitored_clusters_info_names = {cluster['name'] for cluster in monitored_clusters_info}

        return list(
            filter(
                lambda cluster: cluster.name not in monitored_clusters_info_names,
                self._clusters
            )
        )

    def detect_deleted_clusters(self) -> List[Cluster]:
        clusters_map: Dict[str, Cluster] = {cluster.name: cluster for cluster in self._clusters}
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


@attr.s(auto_attribs=True)
class ClusterGroupBuilder:
    _cluster_repository: ClusterRepository

    def build(self, clusters: List[Cluster]) -> ClusterGroup:
        return ClusterGroup(
            clusters=clusters,
            cluster_repository=self._cluster_repository
        )





