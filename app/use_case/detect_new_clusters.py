import attr
from typing import List

from app.model.entities import Cluster
from app.data.repository.cluster import ClusterRepository
from app.data.datasource import ClusterDatasource


@attr.s(auto_attribs=True)
class DetectNewClustersUseCase:
    _cluster_repository: ClusterRepository

    def execute(self, datasource: ClusterDatasource) -> List[Cluster]:
        clusters = datasource.get_clusters()

        monitored_clusters_info = self._cluster_repository.list_clusters_info()
        monitored_clusters_info_names = {cluster['name'] for cluster in monitored_clusters_info}

        return list(
                    filter(
                        lambda cluster: cluster.name not in monitored_clusters_info_names,
                        clusters
                    )
        )
