from injector import Module, provider, singleton

from argocd_client.api_client import ApiClient
from argocd_client.api.cluster_service_api import ClusterServiceApi
from argocd_client.configuration import Configuration
from argocd_client.api import SessionServiceApi
from argocd_client import SessionSessionCreateRequest, SessionSessionResponse, ApplicationServiceApi


from helper import Config


class ArgoModule(Module):

    @provider
    @singleton
    def provide_argo_session(self, config: Config, configuration: Configuration) -> SessionSessionResponse:
        request_auth = SessionSessionCreateRequest(username=config.argo_username, password=config.argo_password)
        session_service = SessionServiceApi(ApiClient(configuration=configuration))
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
    def provide_argo_api_client(self, session: SessionSessionResponse, configuration: Configuration) -> ApiClient:
        api_client = ApiClient(
            configuration=configuration,
            header_name="Authorization",
            header_value=f"Bearer {session.token}"
        )
        return api_client

    @provider
    @singleton
    def provide_cluster_service(self, api_client: ApiClient) -> ClusterServiceApi:
        service_api = ClusterServiceApi(api_client)
        return service_api

    @provider
    @singleton
    def provide_application_service(self, api_client: ApiClient) -> ApplicationServiceApi:
        application_service = ApplicationServiceApi(api_client)
        return application_service

