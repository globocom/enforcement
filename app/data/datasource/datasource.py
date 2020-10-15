from typing import List
import attr

from app.model.entities import Cluster, EnforcementSource
from app.helper.config import Config


@attr.s(auto_attribs=True)
class ClusterDatasource:
    config: Config
    source: EnforcementSource

    def get_clusters(self) -> List[Cluster]:
        raise Exception('Not implement')


