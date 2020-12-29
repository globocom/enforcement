from kubernetes import config
from kubernetes.client import CoreV1Api, V1Secret
import base64


class KubernetesHelper:
    api: CoreV1Api

    def get_namespaced_secret(self, secret_name: str, namespace: str) -> V1Secret:
        return self.api.read_namespaced_secret(secret_name, namespace)

    @staticmethod
    def get_kubernetes_api() -> CoreV1Api:
        config.load_kube_config()
        return CoreV1Api()

    def decode_secret(secret: V1Secret) -> dict:
        return {k: base64.b64decode(v).decode() for k, v in secret._data.items()}
