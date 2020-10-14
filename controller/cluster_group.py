from injector import inject
from typing import ClassVar
from dataclasses import dataclass
import kopf
from controller.base_controller import BaseController
from data.datasource.locator import ClusterDataSourceLocator
from model.entities import ClusterGroup
from model.cluster_monitor import ClusterMonitor


@inject
@dataclass
class ClusterGroupController(BaseController):
    _datasource_locator: ClusterDataSourceLocator
    _cluster_monitor: ClusterMonitor
    KIND: ClassVar[str] = 'clustergroups'

    def create(self, spec: dict, name: str, namespace: str, body: dict, logger, **kwargs):
        cluster_datasource = self._datasource_locator.locate(spec['source'])
        cluster_group = ClusterGroup(**spec)

        clusters_list = cluster_datasource.get_clusters(cluster_group.source)

        new_clusters = self._cluster_monitor.detect_new_clusters(clusters_list)

        logger.info(f"new clusters %s", new_clusters)

    def register(self):
        self.register_method(kopf.on.create, self.create, self.KIND)

