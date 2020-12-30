import base64
import attr

from kubernetes.client import CoreV1Api, V1Secret


@attr.s(auto_attribs=True)
class KubernetesHelper:
    _core_api: CoreV1Api

    def get_namespaced_secret(self, secret_name: str, namespace: str) -> V1Secret:
        return self._core_api.read_namespaced_secret(secret_name, namespace)

    def decode_secret(self, secret: V1Secret) -> dict:
        return {k: base64.b64decode(v).decode() for k, v in secret._data.items()}

    def get_secret_and_decode(self, secret_name: str, namespace: str) -> dict:
        secret = self.get_namespaced_secret(secret_name, namespace)
        decoded_secret = self.decode_secret(secret)
        return decoded_secret