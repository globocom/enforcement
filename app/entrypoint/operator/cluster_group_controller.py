from injector import inject
from typing import ClassVar, List
import kopf
import attr

from app.entrypoint.operator.base_controller import BaseController
from app.domain.entities import ClusterRule, ClusterRuleStatus, Cluster
from app.domain.use_case import ApplyRulesUseCase, SyncRulesUseCase


@inject
@attr.s(auto_attribs=True)
class ClusterGroupController(BaseController):
    _apply_rules_use_case: ApplyRulesUseCase
    _sync_rules_use_case: SyncRulesUseCase
    KIND: ClassVar[str] = 'clusterrules'

    def sync(self, name: str, spec: dict, status: dict, logger, **kwargs):
        logger.debug(f"sync clusters for %s", name)

        current_status = ClusterGroupController._restore_status(status)
        current_clusters = [
            Cluster(name=cluster['name'], url=cluster['url'], id='', token='')
            for cluster in current_status.clusters
        ]
        cluster_rule = ClusterRule(**spec)
        current_clusters = self._sync_rules_use_case.execute(cluster_rule, current_clusters)

        new_status = ClusterGroupController._make_status(current_clusters)

        if new_status != current_status.dict():
            return new_status

    def create(self, spec: dict, **kwargs):
        cluster_rule = ClusterRule(**spec)
        clusters_list = self._apply_rules_use_case.execute(cluster_rule)

        return ClusterGroupController._make_status(clusters_list)

    def register(self):
        self.register_method(kopf.on.create, self.create, self.KIND, id='create')
        self.register_method(kopf.on.timer, self.sync, self.KIND, id='sync', interval=5, idle=10, initial_delay=15)

    @classmethod
    def _make_status(cls, clusters: List[Cluster]) -> dict:
        status = ClusterRuleStatus(
            clusters=[
                {"name": cluster.name, "url": cluster.url} for cluster in clusters
            ]
        )
        return status.dict()

    @classmethod
    def _restore_status(cls, status: dict) -> ClusterRuleStatus:
        current_status = status.get('sync') or status.get('create')
        return ClusterRuleStatus(**current_status)



