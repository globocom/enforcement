import attr
from typing import List

from app.data.repository.cluster import ClusterRepository
from app.model.entities import Cluster


@attr.s(auto_attribs=True)
class RegisterClustersUseCase:
    _cluster_repository: ClusterRepository

    def execute(self, clusters: List[Cluster]):
        for cluster in clusters:
            self._cluster_repository.register_cluster(cluster)


