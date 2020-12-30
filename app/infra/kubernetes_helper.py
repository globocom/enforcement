import base64
import attr

<<<<<<< HEAD
from typing import Dict
from kubernetes.client import CoreV1Api, V1Secret
from app.domain.entities import EnforcementSource, SecretSource

=======
from injector import inject
from kubernetes.client import CoreV1Api, V1Secret

@inject
>>>>>>> 70a7eeced76b8d8a254c4e5c2cca013059cf1d4d
@attr.s(auto_attribs=True)
class KubernetesHelper:
    _core_api: CoreV1Api

    def get_namespaced_secret(self, secret_name: str, namespace: str) -> V1Secret:
        return self._core_api.read_namespaced_secret(secret_name, namespace)

<<<<<<< HEAD
    def decode_secret(self, secret: V1Secret) -> Dict[str, str]:
        return {k: base64.b64decode(v).decode() for k, v in secret._data.items()}

    def get_secret_and_return_decoded(self, source: EnforcementSource) -> Dict[str, str]:
        secret = self.get_namespaced_secret(source.rancher.secretName, 'default')
        return self.decode_secret(secret)
=======
    def decode_secret(self, secret: V1Secret) -> dict:
        return {k: base64.b64decode(v).decode() for k, v in secret._data.items()}

    def get_secret_and_decode(self, secret_name: str, namespace: str) -> dict:
        secret = self.get_namespaced_secret(secret_name, namespace)
        decoded_secret = self.decode_secret(secret)
        return decoded_secret
>>>>>>> 70a7eeced76b8d8a254c4e5c2cca013059cf1d4d
