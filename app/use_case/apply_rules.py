import attr
from typing import List
from app.data.datasource import ClusterDataSourceLocator
from app.model.entities import ClusterGroup, Cluster
from app.use_case.register_clusters import RegisterClustersUseCase
from app.use_case.apply_enforcements import ApplyEnforcementsUseCase


@attr.s(auto_attribs=True)
class ApplyRulesUseCase:
    _datasource_locator: ClusterDataSourceLocator
    _register_clusters_use_case: RegisterClustersUseCase
    _apply_enforcements_use_case: ApplyEnforcementsUseCase

    def execute(self, cluster_group: ClusterGroup) -> List[Cluster]:
        cluster_datasource = self._datasource_locator.locate(cluster_group.source)
        clusters_list = cluster_datasource.get_clusters()
        self._register_clusters_use_case.execute(clusters_list)
        self._apply_enforcements_use_case.execute(clusters_list, cluster_group.enforcements)

        return clusters_list

