from injector import Module, provider, singleton
from app.infra.kubernetes_helper import KubernetesHelper
from kubernetes import config
from kubernetes.client import CoreV1Api

class InfraModule(Module):
    
    @provider
    @singleton
    def provide_kubernetes_helper(self, core_api: CoreV1Api) -> KubernetesHelper:
        return KubernetesHelper(core_api=core_api)

    @provider
    @singleton
    def provide_core_v1_api(self) -> CoreV1Api:
        config.load_incluster_config()
        return CoreV1Api()