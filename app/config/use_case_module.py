from injector import Module, provider, singleton

from app.domain.source_locator import SourceLocator
from app.domain.repositories import EnforcementRepository
from app.domain.use_case import ApplyRulesUseCase, SyncRulesUseCase, UpdateRulesUseCase
from app.domain.cluster_group_builder import ClusterGroupBuilder


class UseCaseModule(Module):

    @provider
    @singleton
    def provider_apply_rules(
            self, locator: SourceLocator, enforcement_repo: EnforcementRepository,
             cluster_group_builder: ClusterGroupBuilder
    ) -> ApplyRulesUseCase:
        return ApplyRulesUseCase(
            enforcement_repository=enforcement_repo,
            source_locator=locator,
            cluster_group_builder=cluster_group_builder
        )

    @provider
    @singleton
    def provider_sync_rules(
            self, locator: SourceLocator, enforcement_repo: EnforcementRepository,
            cluster_group_builder: ClusterGroupBuilder
    ) -> SyncRulesUseCase:
        return SyncRulesUseCase(
            enforcement_repository=enforcement_repo,
            cluster_group_builder=cluster_group_builder,
            source_locator=locator
        )

    @provider
    @singleton
    def provider_update_rules(self, enforcement_repo: EnforcementRepository,
                              cluster_group_builder: ClusterGroupBuilder) -> UpdateRulesUseCase:
        return UpdateRulesUseCase(
            enforcement_repository=enforcement_repo,
            cluster_group_builder=cluster_group_builder
        )

