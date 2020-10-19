from injector import Module, provider, singleton

from app.domain.repositories import ClusterRepository, EnforcementRepository
from app.domain.cluster_group import ClusterGroup, ClusterGroupBuilder
from app.domain.enforcement_installer import EnforcementInstallerBuilder


class DomainModule(Module):
    @provider
    @singleton
    def provide_enforcement_installer_builder(self, repository: EnforcementRepository) -> EnforcementInstallerBuilder:
        return EnforcementInstallerBuilder(
            enforcement_repository=repository
        )

    @provider
    @singleton
    def provide_cluster_group_builder(self, repository: ClusterRepository) -> ClusterGroupBuilder:
        return ClusterGroupBuilder(
            cluster_repository=repository,
        )
