from injector import Module, provider, singleton

from app.domain.source_locator import SourceLocator
from app.domain.cluster_group import ClusterGroupBuilder
from app.domain.enforcement_installer import EnforcementInstallerBuilder

from app.domain.use_case import ApplyRulesUseCase, SyncRulesUseCase


class UseCaseModule(Module):

    @provider
    @singleton
    def provider_apply_rules(
            self, cg_builder: ClusterGroupBuilder, locator: SourceLocator,
            ei_builder: EnforcementInstallerBuilder
    ) -> ApplyRulesUseCase:
        return ApplyRulesUseCase(
            cluster_group_builder=cg_builder,
            enforcements_installer_builder=ei_builder,
            source_locator=locator
        )

    # @provider
    # @singleton
    # def provider_sync_rules(
    #         self, detect_new_clusters: DetectNewClustersUseCase, apply_enforcements: ApplyEnforcementsUseCase,
    #         locator: SourceLocatorImpl
    # ) -> SyncRulesUseCase:
    #     return SyncRulesUseCase(
    #         datasource_locator=locator,
    #         apply_enforcements_use_case=apply_enforcements,
    #         detect_new_clusters_use_case=detect_new_clusters
    #     )

