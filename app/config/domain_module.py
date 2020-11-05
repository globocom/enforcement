from injector import Module, provider, singleton

from app.domain.repositories import ClusterRepository, ProjectRepository
from app.domain.cluster_group_builder import ClusterGroupBuilder

class DomainModule(Module):
    @provider
    @singleton
    def provide_cluster_group_builder(self, cluster_repository: ClusterRepository, project_repository: ProjectRepository) -> ClusterGroupBuilder:
        return ClusterGroupBuilder(cluster_repository=cluster_repository, project_repository=project_repository)