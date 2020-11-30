import attr
from typing import List
from app.domain.entities import ClusterRule, Cluster
from app.domain.source_locator import SourceLocator
from app.domain.repositories import EnforcementRepository
from app.domain.cluster_group_builder import ClusterGroupBuilder

from app.domain.enforcement_installer import EnforcementInstaller


@attr.s(auto_attribs=True)
class ApplyRulesUseCase:
    _source_locator: SourceLocator
    _enforcement_repository: EnforcementRepository
    _cluster_group_builder: ClusterGroupBuilder

    def execute(self, cluster_rule: ClusterRule) -> List[Cluster]:
        source = self._source_locator.locate(cluster_rule.source)
        clusters = source.get_clusters()
        cluster_group = self._cluster_group_builder.build(clusters=clusters)
        cluster_group.register()
        
        enforcement_installer = EnforcementInstaller(
            enforcement_repository=self._enforcement_repository,
            enforcements=cluster_rule.enforcements,
            cluster_group=cluster_group
        )
        enforcement_installer.install()

        return cluster_group.clusters

