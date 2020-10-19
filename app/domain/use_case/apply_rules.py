import attr
from typing import List
from app.domain.entities import ClusterRule, Cluster
from app.domain.source_locator import SourceLocator
from app.domain.repositories import EnforcementRepository, ClusterRepository
from app.domain.cluster_group import ClusterGroup
from app.domain.enforcement_installer import EnforcementInstaller


@attr.s(auto_attribs=True)
class ApplyRulesUseCase:
    _source_locator: SourceLocator
    _enforcement_repository: EnforcementRepository
    _cluster_repository: ClusterRepository

    def execute(self, cluster_rule: ClusterRule) -> List[Cluster]:
        source = self._source_locator.locate(cluster_rule.source)
        clusters = source.get_clusters()
        cluster_group = ClusterGroup(clusters=clusters, cluster_repository=self._cluster_repository)
        cluster_group.register()
        enforcement_installer = EnforcementInstaller(
            enforcement_repository=self._enforcement_repository,
            enforcements=cluster_rule.enforcements,
            cluster_group=cluster_group
        )
        enforcement_installer.install()

        return cluster_group.clusters

