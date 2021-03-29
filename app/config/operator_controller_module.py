from injector import Module, provider, singleton

from app.entrypoint.operator.controller import ClusterRuleController, StatusManager
from app.domain.use_case.apply_rules import ApplyRulesUseCase
from app.domain.use_case.sync_rules import SyncRulesUseCase
from app.domain.use_case.update_rules import UpdateRulesUseCase

from app.infra.config import Config
from app.infra.kubernetes_helper import KubernetesHelper


class OperatorControllerModule(Module):

    @provider
    @singleton
    def provide_cluster_rule_controller(self, status_manager: StatusManager,
                                        uc_apply: ApplyRulesUseCase,
                                        uc_sync: SyncRulesUseCase,
                                        uc_update: UpdateRulesUseCase) -> ClusterRuleController:
        return ClusterRuleController(
            status_manager=status_manager,
            apply_rules_use_case=uc_apply,
            sync_rules_use_case=uc_sync,
            update_rules_use_case=uc_update,
        )

    @provider
    @singleton
    def provide_status_manager(self, cfg: Config, helper: KubernetesHelper) -> StatusManager:
        return StatusManager(config=cfg, kubernetes_helper=helper)
