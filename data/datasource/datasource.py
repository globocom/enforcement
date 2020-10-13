from typing import List

from model.entities import Cluster, EnforcementSource
from helper.config import Config


class ClusterDatasource:
    def __init__(self, config: Config):
        self._config = config

    def get_clusters(self, source: EnforcementSource) -> List[Cluster]:
        raise Exception('Not implement')


