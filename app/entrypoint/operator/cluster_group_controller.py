from injector import inject
from typing import ClassVar
import kopf
import attr

from app.entrypoint.operator.base_controller import BaseController
from app.domain.entities import ClusterRule, ClusterRuleStatus
from app.domain.use_case import ApplyRulesUseCase


@inject
@attr.s(auto_attribs=True)
class ClusterGroupController(BaseController):
    _apply_rules_use_case: ApplyRulesUseCase
    KIND: ClassVar[str] = 'clusterrules'

    def create(self, spec: dict, name: str, namespace: str, body: dict, logger, **kwargs):
        cluster_rule = ClusterRule(**spec)
        clusters_list = self._apply_rules_use_case.execute(cluster_rule)

        status = ClusterRuleStatus(clusters=[cluster.name for cluster in clusters_list])
        return status.dict()

    def register(self):
        self.register_method(kopf.on.create, self.create, self.KIND)

