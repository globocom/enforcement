from injector import inject
from typing import ClassVar
import kopf
import attr

from app.controller.base_controller import BaseController
from app.model.entities import ClusterGroup, ClusterGroupStatus
from app.use_case import ApplyRulesUseCase


@inject
@attr.s(auto_attribs=True)
class ClusterGroupController(BaseController):
    _apply_rules_use_case: ApplyRulesUseCase
    KIND: ClassVar[str] = 'clustergroups'

    def create(self, spec: dict, name: str, namespace: str, body: dict, logger, **kwargs):
        cluster_group = ClusterGroup(**spec)
        clusters_list = self._apply_rules_use_case.execute(cluster_group)

        status = ClusterGroupStatus(clusters=[cluster.name for cluster in clusters_list])
        return status.dict()

    def register(self):
        self.register_method(kopf.on.create, self.create, self.KIND)

