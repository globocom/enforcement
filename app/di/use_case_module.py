from injector import Module, provider, singleton

from app.use_case.register_clusters import RegisterClustersUseCase
from app.use_case.apply_rules import ApplyRulesUseCase
from app.use_case.apply_enforcements import ApplyEnforcementsUseCase
from app.use_case.detect_new_clusters import DetectNewClustersUseCase
from app.use_case.sync_rules import SyncRulesUseCase

from app.data.repository.cluster import ClusterRepository
from app.data.repository.enforcement import EnforcementRepository
from app.data.datasource.locator import ClusterDataSourceLocator


class UseCaseModule(Module):
    @provider
    @singleton
    def provide_register_clusters(self, cluster_repository: ClusterRepository) -> RegisterClustersUseCase:
        return RegisterClustersUseCase(cluster_repository=cluster_repository)

    @provider
    @singleton
    def provider_apply_rules(
            self, register_clusters: RegisterClustersUseCase, locator: ClusterDataSourceLocator,
            applly_enforcements: ApplyEnforcementsUseCase
    ) -> ApplyRulesUseCase:
        return ApplyRulesUseCase(
            datasource_locator=locator,
            register_clusters_use_case=register_clusters,
            apply_enforcements_use_case=applly_enforcements
        )

    @provider
    @singleton
    def provider_sync_rules(
            self, detect_new_clusters: DetectNewClustersUseCase, apply_enforcements: ApplyEnforcementsUseCase,
            locator: ClusterDataSourceLocator
    ) -> SyncRulesUseCase:
        return SyncRulesUseCase(
            datasource_locator=locator,
            apply_enforcements_use_case=apply_enforcements,
            detect_new_clusters_use_case=detect_new_clusters
        )

    @provider
    @singleton
    def provider_apply_enforcements(self, enforcement_repository: EnforcementRepository) -> ApplyEnforcementsUseCase:
        return ApplyEnforcementsUseCase(enforcement_repository=enforcement_repository)

    @provider
    @singleton
    def provider_detect_new_clusters(self, cluster_repository: ClusterRepository) -> DetectNewClustersUseCase:
        return DetectNewClustersUseCase(
            cluster_repository=cluster_repository
        )

