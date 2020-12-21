from injector import inject
from typing import ClassVar, List
import kopf
import attr

from app.entrypoint.operator.base_controller import BaseController
from app.domain.entities import ClusterRule, ClusterRuleStatus, Cluster, Enforcement
from app.domain.use_case import ApplyRulesUseCase, SyncRulesUseCase, UpdateRulesUseCase, RulesResponse


@inject
@attr.s(auto_attribs=True)
class ClusterRuleController(BaseController):
    _apply_rules_use_case: ApplyRulesUseCase
    _sync_rules_use_case: SyncRulesUseCase
    _update_rules_use_case: UpdateRulesUseCase
    KIND: ClassVar[str] = 'clusterrules'

    def update(self, old: List[dict], new: List[dict], status: dict, **kwargs):
        if not old:
            return

        old_enforcement_list = ClusterRuleController._make_enforcement_list(old)
        new_enforcement_list = ClusterRuleController._make_enforcement_list(new)
        current_status = ClusterRuleController._restore_status(status)

        current_clusters = [
            Cluster(name=cluster['name'], url=cluster['url'], id='', token='')
            for cluster in current_status.clusters
        ]

        self._update_rules_use_case.execute(
            clusters=current_clusters,
            old_enforcements=old_enforcement_list,
            new_enforcements=new_enforcement_list,
        )

    def sync(self, name: str, spec: dict, status: dict, logger, **kwargs):
        logger.debug(f"sync clusters for %s", name)

        current_status = ClusterRuleController._restore_status(status)
        current_clusters = [
            Cluster(name=cluster['name'], url=cluster['url'], id='', token='')
            for cluster in current_status.clusters
        ]
        cluster_rule = ClusterRule(**spec)
        response = self._sync_rules_use_case.execute(cluster_rule, current_clusters)

        new_status = ClusterRuleController._make_status(response)

        if new_status != current_status.dict():
            return new_status

    def create(self, spec: dict, **kwargs):
        cluster_rule = ClusterRule(**spec)
        response = self._apply_rules_use_case.execute(cluster_rule)

        return ClusterRuleController._make_status(response)

    def register(self):
        self.register_method(kopf.on.create, self.create, self.KIND, id='create')
        self.register_method(kopf.on.field, self.update, self.KIND, id='update', field='spec.enforcements')
        self.register_method(kopf.on.timer, self.sync, self.KIND, id='sync', interval=6, initial_delay=15, idle=10)

    @classmethod
    def _make_enforcement_list(cls, enforcement_map_list) -> List[Enforcement]:
        if not enforcement_map_list:
            return []
        return [Enforcement(**enforcement_map) for enforcement_map in enforcement_map_list]

    @classmethod
    def _make_status(cls, response: RulesResponse) -> dict:
        status = ClusterRuleStatus(
            install_errors=[
                enforcement.name for enforcement in response.install_errors
            ],
            clusters=[
                {"name": cluster.name, "url": cluster.url} for cluster in response.clusters
            ]
        )
        return status.dict()

    @classmethod
    def _restore_status(cls, status: dict) -> ClusterRuleStatus:
        current_status = status.get('sync') or status.get('create')
        return ClusterRuleStatus(**current_status)



