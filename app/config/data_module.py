from injector import Module, provider, singleton
from argocd_client import (
    SessionSessionCreateRequest,
    SessionSessionResponse,
    ApplicationServiceApi,
)
from argocd_client.api import SessionServiceApi
from argocd_client.api_client import ApiClient
from argocd_client.configuration import Configuration
from argocd_client.api.cluster_service_api import ClusterServiceApi

from app.infra.config import Config

from app.domain.repositories import ClusterRepository, EnforcementRepository
from app.domain.source_locator import SourceLocator

from app.data.argo.cluster import ClusterService
from app.data.argo.application import ApplicationService
from app.data.source.definition.locator import SourceLocatorImpl


class DataModule(Module):

    @provider
    @singleton
    def provide_argo_session(
            self, config: Config, configuration: Configuration,
    ) -> SessionSessionResponse:
        request_auth = SessionSessionCreateRequest(
            username=config.argo_username,
            password=config.argo_password
        )
        session_service = SessionServiceApi(
            ApiClient(configuration=configuration)
        )
        return session_service.create_mixin11(request_auth)

    @provider
    @singleton
    def provide_argo_configuration(self, config: Config) -> Configuration:
        configuration = Configuration(
            host=config.argo_url,
        )
        configuration.verify_ssl = False
        return configuration

    @provider
    @singleton
    def provide_argo_api_client(
            self, session: SessionSessionResponse, configuration: Configuration,
    ) -> ApiClient:
        return ApiClient(
            configuration=configuration,
            header_name="Authorization",
            header_value=f"Bearer {session.token}"
        )

    @provider
    @singleton
    def provide_cluster_service(self, api_client: ApiClient) -> ClusterServiceApi:
        return ClusterServiceApi(api_client)

    @provider
    @singleton
    def provide_application_service(self, api_client: ApiClient) -> ApplicationServiceApi:
        return ApplicationServiceApi(api_client)

    @provider
    @singleton
    def provide_cluster_repository(self, cluster_service: ClusterServiceApi) -> ClusterRepository:
        return ClusterService(cluster_service=cluster_service)

    @provider
    @singleton
    def provide_enforcement_repository(self, application_service: ApplicationServiceApi) -> EnforcementRepository:
        return ApplicationService(application_service=application_service)

    @provider
    @singleton
    def provide_source_locator(self, config: Config) -> SourceLocator:
        return SourceLocatorImpl(config_helper=config)
