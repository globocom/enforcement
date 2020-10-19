import attr
from typing import List

from app.domain.entities import ClusterRule, Cluster
from app.domain.source_locator import SourceLocator
from app.domain.repositories import EnforcementRepository, ClusterRepository


@attr.s(auto_attribs=True)
class SyncRulesUseCase:
    _source_locator: SourceLocator
    _cluster_repository: ClusterRepository
    _enforcement_repository: EnforcementRepository

    def execute(self, cluster_rule: ClusterRule, current_clusters: List[Cluster]) -> List[Cluster]:
        source_repository = self._source_locator.locate(cluster_rule.source)
        source_clusters = source_repository.get_clusters()

        source_cluster_group = self._cluster_group_builder.build(source_clusters)
        current_cluster_group = self._cluster_group_builder.build(current_clusters)


