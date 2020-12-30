import base64
import attr

from typing import Dict
from kubernetes.client import CoreV1Api, V1Secret
from app.domain.entities import EnforcementSource, SecretSource

@attr.s(auto_attribs=True)
class KubernetesHelper:
    _core_api: CoreV1Api

    def get_namespaced_secret(self, secret_name: str, namespace: str) -> V1Secret:
        return self._core_api.read_namespaced_secret(secret_name, namespace)

    def decode_secret(self, secret: V1Secret) -> Dict[str, str]:
        return {k: base64.b64decode(v).decode() for k, v in secret._data.items()}

    def get_secret_and_return_decoded(self, source: EnforcementSource) -> Dict[str, str]:
        secret = self.get_namespaced_secret(source.rancher.secretName, 'default')
        return self.decode_secret(secret)
