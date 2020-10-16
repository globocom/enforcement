import attr
from typing import List

from app.use_case.detect_new_clusters import DetectNewClustersUseCase
from app.use_case.apply_enforcements import ApplyEnforcementsUseCase

from app.model.entities import Cluster, ClusterGroup

from app.data.datasource import ClusterDataSourceLocator


@attr.s(auto_attribs=True)
class SyncRulesUseCase:
    _detect_new_clusters_use_case: DetectNewClustersUseCase
    _apply_enforcements_use_case: ApplyEnforcementsUseCase
    _datasource_locator: ClusterDataSourceLocator

    def execute(self, cluster_group: ClusterGroup) -> List[Cluster]:
        datasource = self._datasource_locator.locate(cluster_group.source)
        new_clusters_list = self._detect_new_clusters_use_case.execute(datasource)
        self._apply_enforcements_use_case.execute(new_clusters_list, cluster_group.enforcements)
        return new_clusters_list

