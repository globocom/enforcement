from typing import List

import attr

from app.domain.cluster_group_builder import ClusterGroupBuilder
from app.domain.enforcement_installer_builder import EnforcementInstallerBuilder
from app.domain.entities import ClusterRule, Cluster
from app.domain.repositories import EnforcementRepository
from app.domain.source_locator import SourceLocator


@attr.s(auto_attribs=True)
class ApplyRulesUseCase:
    _source_locator: SourceLocator
    _enforcement_repository: EnforcementRepository
    _cluster_group_builder: ClusterGroupBuilder
    _enforcement_installer_builder: EnforcementInstallerBuilder

    def execute(self, cluster_rule: ClusterRule) -> List[Cluster]:
        source = self._source_locator.locate(cluster_rule.source)
        clusters = source.get_clusters()
        cluster_group = self._cluster_group_builder.build(clusters=clusters)
        cluster_group.register()

        enforcement_installer = self._enforcement_installer_builder.build(
            enforcements=cluster_rule.enforcements,
            cluster_group=cluster_group
        )
        enforcement_installer.install()

        return cluster_group.clusters
