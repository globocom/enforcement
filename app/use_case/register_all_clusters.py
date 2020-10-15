import attr
from typing import List
from app.data.datasource import ClusterDataSourceLocator
from app.model.entities import EnforcementSource, Cluster
from app.use_case.register_clusters import RegisterClustersUseCase


@attr.s(auto_attribs=True)
class RegisterAllClustersUseCase:
    _datasource_locator: ClusterDataSourceLocator
    _register_clusters_use_case: RegisterClustersUseCase

    def execute(self, source: EnforcementSource) -> List[Cluster]:
        cluster_datasource = self._datasource_locator.locate(source)
        clusters_list = cluster_datasource.get_clusters()
        self._register_clusters_use_case.execute(clusters_list)
        return clusters_list

