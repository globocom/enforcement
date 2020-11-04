import attr
from typing import List

from app.domain.entities import ClusterRule, Cluster
from app.domain.source_locator import SourceLocator
from app.domain.repositories import EnforcementRepository, ClusterRepository, ProjectRepository
from app.domain.cluster_group import ClusterGroup
from app.domain.enforcement_installer import EnforcementInstaller


@attr.s(auto_attribs=True)
class SyncRulesUseCase:
    _source_locator: SourceLocator
    _cluster_repository: ClusterRepository
    _enforcement_repository: EnforcementRepository
    _project_repository: ProjectRepository

    def execute(self, cluster_rule: ClusterRule, current_clusters: List[Cluster]) -> List[Cluster]:
        source_repository = self._source_locator.locate(cluster_rule.source)
        source_clusters = source_repository.get_clusters()

        source_cluster_group = ClusterGroup(clusters=source_clusters, cluster_repository=self._cluster_repository)
        current_cluster_group = ClusterGroup(clusters=current_clusters, cluster_repository=self._cluster_repository)

        deleted_clusters = current_cluster_group - source_cluster_group
        enforcement_uninstall = EnforcementInstaller(
            enforcement_repository=self._enforcement_repository,
            cluster_group=deleted_clusters,
            enforcements=cluster_rule.enforcements
        )

        enforcement_uninstall.uninstall()
        deleted_clusters.unregister()

        for deleted_cluster in deleted_clusters.clusters:
            self._project_repository.remove_project(deleted_cluster.name)

        new_clusters = source_cluster_group - current_cluster_group
        new_clusters.register()

        for new_cluster in new_clusters.clusters:
            self._project_repository.create_project(new_cluster)

        enforcement_installer = EnforcementInstaller(
            enforcement_repository=self._enforcement_repository,
            cluster_group=new_clusters,
            enforcements=cluster_rule.enforcements
        )

        enforcement_installer.install()
        return source_clusters



