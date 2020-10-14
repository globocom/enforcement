from injector import inject
from typing import ClassVar
from dataclasses import dataclass
import kopf
from controller.base_controller import BaseController
from data.datasource.locator import ClusterDataSourceLocator
from model.entities import ClusterGroup, ClusterGroupStatus
from model.cluster_monitor import ClusterMonitor
from data.repository.enforcement import EnforcementRepository


@inject
@dataclass
class ClusterGroupController(BaseController):
    _datasource_locator: ClusterDataSourceLocator
    _cluster_monitor: ClusterMonitor
    _enforcement_repository: EnforcementRepository
    KIND: ClassVar[str] = 'clustergroups'

    def create(self, spec: dict, name: str, namespace: str, body: dict, logger, **kwargs):
        cluster_datasource = self._datasource_locator.locate(spec['source'])
        cluster_group = ClusterGroup(**spec)

        clusters_list = cluster_datasource.get_clusters(cluster_group.source)

        for cluster in clusters_list:
            self._cluster_monitor.register(cluster)
            enforcements_list = self._enforcement_repository.list_installed_enforcements(cluster_name=cluster.name)
            installed_enforcements_names = {
                enforcement.name: enforcement for enforcement in enforcements_list
            }
            for enforcement in cluster_group.enforcements:
                if enforcement.name not in installed_enforcements_names:
                    self._enforcement_repository.create_enforcement(cluster.name, enforcement)
                elif enforcement != installed_enforcements_names[enforcement.name]:
                    self._enforcement_repository.update_enforcement(cluster.name, enforcement)

        status = ClusterGroupStatus(clusters=[cluster.name for cluster in clusters_list])
        return status.dict()

    def register(self):
        self.register_method(kopf.on.create, self.create, self.KIND)

