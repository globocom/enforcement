from injector import Module, provider, singleton

from app.domain.source_locator import SourceLocator
from app.domain.repositories import ClusterRepository, EnforcementRepository, ProjectRepository
from app.domain.use_case import ApplyRulesUseCase, SyncRulesUseCase, UpdateRulesUseCase


class UseCaseModule(Module):

    @provider
    @singleton
    def provider_apply_rules(
            self, cluster_repo: ClusterRepository, locator: SourceLocator,
            enforcement_repo: EnforcementRepository, project_repo: ProjectRepository
    ) -> ApplyRulesUseCase:
        return ApplyRulesUseCase(
            cluster_repository=cluster_repo,
            enforcement_repository=enforcement_repo,
            project_repository=project_repo,
            source_locator=locator
        )

    @provider
    @singleton
    def provider_sync_rules(
            self, cluster_repo: ClusterRepository, locator: SourceLocator,
            enforcement_repo: EnforcementRepository, project_repo: ProjectRepository
    ) -> SyncRulesUseCase:
        return SyncRulesUseCase(
            cluster_repository=cluster_repo,
            enforcement_repository=enforcement_repo,
            project_repository=project_repo,
            source_locator=locator
        )

    @provider
    @singleton
    def provider_update_rules(self, enforcement_repo: EnforcementRepository,
                              cluster_repo: ClusterRepository) -> UpdateRulesUseCase:
        return UpdateRulesUseCase(
            enforcement_repository=enforcement_repo,
            cluster_repository=cluster_repo
        )

