import attr

from app.domain.entities import EnforcementSource, Secret
from app.domain.repositories import SourceRepository
from app.infra.config import Config
from app.data.source.definition.utils import SourceUtils
from app.infra.kubernetes_helper import KubernetesHelper


@attr.s(auto_attribs=True)
class BaseSource(SourceRepository):
    config: Config
    source: EnforcementSource
    kubernetes_helper: KubernetesHelper
    secret: Secret


    def get_secret(self) -> Secret:
        source_name = SourceUtils.get_source_name(self.source)
        secret_name = self.source.secretName if self.source.secretName is not None else source_name

        return self.kubernetes_helper.get_secret(secret_name)


    def __attrs_post_init__(self):
        self.secret = self.get_secret()