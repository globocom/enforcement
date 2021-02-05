import base64
import attr

from typing import Dict
from app.domain.entities import EnforcementSource, Secret
from kubernetes.client import CoreV1Api, V1Secret


@attr.s(auto_attribs=True)
class KubernetesHelper:
    _core_api: CoreV1Api

    def _get_secret_from_api(self, secret_name: str) -> V1Secret:
        secrets = self._core_api.list_secret_for_all_namespaces()
        return [secret for secret in secrets.items
                if secret.metadata.name == secret_name][0]

    def _decode_secret(self, secret: V1Secret) -> Dict[str, str]:
        return {k: base64.b64decode(v).decode() for k, v in secret.data.items()}

    def get_secret(self, secret_name: str) -> Secret:
        secret_encoded = self._get_secret_from_api(secret_name)
        secret_decoded = self._decode_secret(secret_encoded)
        return Secret(**secret_decoded)
