from injector import inject
from typing import Dict, Callable

from app.helper.config import Config
from app.data.datasource.datasource import ClusterDatasource
from app.data.datasource.rancher import RancherDatasource
from app.model.entities import EnforcementSource


class ClusterDataSourceLocator:
    @inject
    def __init__(self, config_helper: Config):
        self._config_helper = config_helper
        self._datasources: Dict[str, Callable] = {
            'rancher': RancherDatasource,
        }

    def locate(self, source: EnforcementSource) -> ClusterDatasource:
        source_name = list(source.__dict__.keys())[0]
        datasource_class = self._datasources[source_name]

        if not datasource_class:
            raise Exception("Source not defined")

        return datasource_class(config=self._config_helper, source=source)
