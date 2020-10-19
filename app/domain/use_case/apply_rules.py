import attr
from typing import List
from app.domain.entities import ClusterRule, Cluster
from app.domain.source_locator import SourceLocator
from app.domain.cluster_group import ClusterGroupBuilder
from app.domain.enforcement_installer import EnforcementInstallerBuilder


@attr.s(auto_attribs=True)
class ApplyRulesUseCase:
    _source_locator: SourceLocator
    _cluster_group_builder: ClusterGroupBuilder
    _enforcements_installer_builder: EnforcementInstallerBuilder

    def execute(self, cluster_rule: ClusterRule) -> List[Cluster]:
        source = self._source_locator.locate(cluster_rule.source)
        clusters = source.get_clusters()
        cluster_group = self._cluster_group_builder.build(clusters)
        cluster_group.register()
        enforcement_installer = self._enforcements_installer_builder.build(cluster_group, cluster_rule.enforcements)
        enforcement_installer.install()

        return cluster_group.clusters

