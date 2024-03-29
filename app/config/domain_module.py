from injector import Module, provider, singleton

from app.domain.cluster_group_builder import ClusterGroupBuilder
from app.domain.enforcement_change_detector_builder import EnforcementChangeDetectorBuilder
from app.domain.enforcement_installer_builder import EnforcementInstallerBuilder
from app.domain.repositories import ClusterRepository, ProjectRepository, EnforcementRepository
from app.domain.enforcement_dynamic_mapper import EnforcementDynamicMapper
from app.domain.triggers import TriggerBase, TriggerService, TriggerBuilder


class DomainModule(Module):

    @provider
    @singleton
    def provide_enforcement_dynamic_mapper(self) -> EnforcementDynamicMapper:
        return EnforcementDynamicMapper()

    @provider
    @singleton
    def provide_trigger_base(self, trigger_service: TriggerService) -> TriggerBase:
        return TriggerBase(trigger_service=trigger_service)

    @provider
    @singleton
    def provide_trigger_builder(self, trigger_base: TriggerBase) -> TriggerBuilder:
        return TriggerBuilder(trigger_base=trigger_base)

    @provider
    @singleton
    def provide_cluster_group_builder(self, cluster_repository: ClusterRepository,
                                      project_repository: ProjectRepository) -> ClusterGroupBuilder:
        return ClusterGroupBuilder(cluster_repository=cluster_repository, project_repository=project_repository)

    @provider
    @singleton
    def provide_enforcement_installer_builder(self,
                                              enforcement_repository: EnforcementRepository,
                                              enforcement_dynamic_mapper: EnforcementDynamicMapper,
                                              trigger_builder: TriggerBuilder) -> EnforcementInstallerBuilder:
        return EnforcementInstallerBuilder(
            enforcement_repository=enforcement_repository,
            enforcement_dynamic_mapper=enforcement_dynamic_mapper,
            trigger_builder=trigger_builder
        )

    @provider
    @singleton
    def provide_enforcement_change_detector_builder(self) -> EnforcementChangeDetectorBuilder:
        return EnforcementChangeDetectorBuilder()
