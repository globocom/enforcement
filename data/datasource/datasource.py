from typing import List
from model.cluster import Cluster


class ClusterDatasource:
    def get_clusters(self, params: dict) -> List[Cluster]:
        raise Exception('Not implement')

