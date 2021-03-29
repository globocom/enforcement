from typing import ClassVar, List

import attr
import kopf

from app.entrypoint.operator.controller.base_controller import BaseController
from app.domain.entities import ClusterRule, ClusterRuleStatus, Cluster, Enforcement
from app.domain.use_case import ApplyRulesUseCase, SyncRulesUseCase, UpdateRulesUseCase, RulesResponse
from app.infra.kubernetes_helper import KubernetesHelper
from app.infra.config import Config


@attr.s(auto_attribs=True)
class StatusManager:
    _kubernetes_helper: KubernetesHelper
    _config: Config

    def get_status(self, kind: str, name: str) -> ClusterRuleStatus:
        status_dto = self._kubernetes_helper.get_custom_resource_status(
            self._config.api_group,
            self._config.api_version,
            kind,
            name
        )

        return ClusterRuleStatus(**status_dto) \
            if status_dto and 'clusters' in status_dto else None

    def update_status(self, kind: str, name: str, status_dto: dict):

        self._kubernetes_helper.update_custom_resource_status(
            status_dto,
            self._config.api_group,
            self._config.api_version,
            kind,
            name,
        )

    @classmethod
    def build_status(cls, response: RulesResponse) -> dict:
        status = ClusterRuleStatus(
            install_errors=[
                enforcement.name for enforcement in response.install_errors
            ],
            clusters=[
                {"name": cluster.name, "url": cluster.url} for cluster in response.clusters
            ]
        )
        return status.dict()


@attr.s(auto_attribs=True)
class ClusterRuleController(BaseController):
    _apply_rules_use_case: ApplyRulesUseCase
    _sync_rules_use_case: SyncRulesUseCase
    _update_rules_use_case: UpdateRulesUseCase
    _status_manager: StatusManager
    KIND: ClassVar[str] = "clusterrules"

    def update(self, name, old: List[dict], new: List[dict], status: dict, logger, **kwargs):
        if not old:
            return

        logger.debug(f"update rules for %s", name)

        old_enforcement_list = ClusterRuleController._make_enforcement_list(old)
        new_enforcement_list = ClusterRuleController._make_enforcement_list(new)
        current_status = self._status_manager.get_status(self.KIND, name)

        current_clusters = [
            Cluster(name=cluster['name'], url=cluster['url'], id='', token='')
            for cluster in current_status.clusters
        ]

        response = self._update_rules_use_case.execute(
            clusters=current_clusters,
            old_enforcements=old_enforcement_list,
            new_enforcements=new_enforcement_list,
        )

        enforcements_change = [
            enforcement.name for enforcement in response.removed_enforcements + response.changed_enforcements
        ]

        response.install_errors = response.install_errors + list(
            map(
                lambda enf_name: Enforcement(name=enf_name, repo=""),
                filter(
                    lambda enforcement_name: enforcement_name not in enforcements_change,
                    current_status.install_errors,
                )
            )
        )

        response.clusters = current_clusters

        self._status_manager.update_status(
            self.KIND,
            name,
            self._status_manager.build_status(response)
        )

    def sync(self, name: str, spec: dict, status: dict, logger, **kwargs):
        logger.debug(f"sync clusters for %s", name)

        current_status = self._status_manager.get_status(self.KIND, name)

        if not current_status:
            return

        current_clusters = [
            Cluster(name=cluster['name'], url=cluster['url'], id='', token='')
            for cluster in current_status.clusters
        ]
        cluster_rule = ClusterRule(**spec)

        response = self._sync_rules_use_case.execute(cluster_rule, current_clusters)
        response.install_errors = [Enforcement(name=name, repo="") for name in current_status.install_errors]

        new_status = self._status_manager.build_status(response)

        if current_status != new_status:
            self._status_manager.update_status(
                self.KIND,
                name,
                new_status
            )

    def create(self, name, spec: dict, **kwargs):
        print(f"create rules for {name}")

        cluster_rule = ClusterRule(**spec)

        response = self._apply_rules_use_case.execute(cluster_rule)

        self._status_manager.update_status(
            self.KIND,
            name,
            self._status_manager.build_status(response)
        )

    @classmethod
    def _make_enforcement_list(cls, enforcement_map_list) -> List[Enforcement]:
        if not enforcement_map_list:
            return []
        return [Enforcement(**enforcement_map) for enforcement_map in enforcement_map_list]
