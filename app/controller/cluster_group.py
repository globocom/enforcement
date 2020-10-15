from injector import inject
from typing import ClassVar
import kopf
import attr

from app.controller.base_controller import BaseController
from app.data.datasource import ClusterDataSourceLocator
from app.model.entities import ClusterGroup, ClusterGroupStatus
from app.model.cluster_monitor import ClusterMonitor
from app.data.repository import EnforcementRepository
from app.use_case import RegisterAllClustersUseCase


@inject
@attr.s(auto_attribs=True)
class ClusterGroupController(BaseController):
    _datasource_locator: ClusterDataSourceLocator
    _cluster_monitor: ClusterMonitor
    _enforcement_repository: EnforcementRepository
    _register_all_clusters_use_case: RegisterAllClustersUseCase
    KIND: ClassVar[str] = 'clustergroups'

    def create(self, spec: dict, name: str, namespace: str, body: dict, logger, **kwargs):
        cluster_group = ClusterGroup(**spec)

        clusters_list = self._register_all_clusters_use_case.execute(cluster_group.source)

        for cluster in clusters_list:
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

