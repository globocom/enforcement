from injector import inject

from helper.config import Config
from data.datasource.datasource import ClusterDatasource
from data.datasource.rancher import RancherDatasource


class ClusterDataSourceLocator:
    @inject
    def __init__(self, config_helper: Config):
        self._datasources = {
            'rancher': RancherDatasource(config_helper)
        }

    def locate(self, source: dict) -> ClusterDatasource:
        source_names = list(source.keys())
        datasource: ClusterDatasource = self._datasources[source_names[0]] \
            if source_names and source_names[0] in self._datasources else None

        if not datasource:
            raise Exception("Source not defined")

        return datasource