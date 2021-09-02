from __future__ import annotations

from typing import List
from argocd_client import ApiException

import attr

from app.domain.entities import Cluster
from app.domain.repositories import ClusterRepository, ProjectRepository


@attr.s(auto_attribs=True)
class ClusterGroup:
    _clusters: List[Cluster]
    _cluster_repository: ClusterRepository
    _project_repository: ProjectRepository

    @property
    def clusters(self):
        return self._clusters

    def register(self):
        clusters_saved = self._cluster_repository.list_clusters_info()
        cluster_saved_names = [cluster["name"] for cluster in clusters_saved]

        for cluster in self._clusters:
            if cluster.name not in cluster_saved_names:
                try:
                    self._cluster_repository.register_cluster(cluster)
                    self._project_repository.create_project(cluster)
                finally:
                    continue

    def unregister(self):
        for cluster in self._clusters:
            try:
                self._cluster_repository.unregister_cluster(cluster)
                self._project_repository.remove_project(cluster.name)
            except ApiException as e:
                if e.status != 404:
                    raise e

    def __sub__(self, other: ClusterGroup) -> ClusterGroup:
        cluster_names = {cluster.name: cluster for cluster in other.clusters}
        result_clusters = list(
            filter(
                lambda cluster: cluster.name not in cluster_names,
                self._clusters
            )
        )

        return ClusterGroup(cluster_repository=self._cluster_repository
                            , project_repository=self._project_repository,
                            clusters=result_clusters)
