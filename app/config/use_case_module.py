from injector import Module, provider, singleton

from app.domain.source_locator import SourceLocator
from app.domain.repositories import ClusterRepository, EnforcementRepository
from app.domain.use_case import ApplyRulesUseCase, SyncRulesUseCase


class UseCaseModule(Module):

    @provider
    @singleton
    def provider_apply_rules(
            self, cluster_repo: ClusterRepository, locator: SourceLocator,
            enforcement_repo: EnforcementRepository
    ) -> ApplyRulesUseCase:
        return ApplyRulesUseCase(
            cluster_repository=cluster_repo,
            enforcement_repository=enforcement_repo,
            source_locator=locator
        )

    @provider
    @singleton
    def provider_sync_rules(
            self, cluster_repo: ClusterRepository, locator: SourceLocator,
            enforcement_repo: EnforcementRepository
    ) -> SyncRulesUseCase:
        return SyncRulesUseCase(
            cluster_repository=cluster_repo,
            enforcement_repository=enforcement_repo,
            source_locator=locator
        )

