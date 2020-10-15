from injector import Module, provider, singleton
from app.use_case.register_clusters import RegisterClustersUseCase
from app.use_case.register_all_clusters import RegisterAllClustersUseCase
from app.data.repository.cluster import ClusterRepository
from app.data.datasource.locator import ClusterDataSourceLocator


class UseCaseModule(Module):
    @provider
    @singleton
    def provide_register_clusters(self, cluster_repository: ClusterRepository) -> RegisterClustersUseCase:
        return RegisterClustersUseCase(cluster_repository=cluster_repository)

    @provider
    @singleton
    def provider_register_all_clusters(
            self, register_clusters: RegisterClustersUseCase, locator: ClusterDataSourceLocator
    ) -> RegisterAllClustersUseCase:
        return RegisterAllClustersUseCase(
            datasource_locator=locator,
            register_clusters_use_case=register_clusters
        )

