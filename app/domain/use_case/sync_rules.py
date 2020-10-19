import attr
from typing import List

from app.domain.entities import ClusterRule, Cluster
from app.domain.source_locator import SourceLocator
from app.domain.cluster_group import ClusterGroupBuilder
from app.domain.enforcement_installer import EnforcementInstallerBuilder


@attr.s(auto_attribs=True)
class SyncRulesUseCase:
    _source_locator: SourceLocator
    _cluster_group_builder: ClusterGroupBuilder
    _enforcements_installer_builder: EnforcementInstallerBuilder

    def execute(self, cluster_rule: ClusterRule) -> List[Cluster]:
        pass

