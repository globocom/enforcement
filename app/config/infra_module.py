from injector import Module, provider, singleton
from app.infra.kubernetes_helper import KubernetesHelper
from kubernetes import config
from kubernetes.client import CoreV1Api
from kubernetes.config.config_exception import ConfigException

from app.infra.config import Config


class InfraModule(Module):
    
    @provider
    @singleton
    def provide_kubernetes_helper(self, core_api: CoreV1Api, config: Config) -> KubernetesHelper:
        return KubernetesHelper(core_api=core_api, current_namespace=config.current_namespace)

    @provider
    @singleton
    def provide_core_v1_api(self) -> CoreV1Api:
        self._load_config()
        return CoreV1Api()

    @classmethod
    def _load_config(cls):
        try:
            config.load_incluster_config()
        except ConfigException:
            config.load_kube_config()
