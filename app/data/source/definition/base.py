import attr

from app.domain.entities import EnforcementSource
from app.domain.repositories import SourceRepository
from app.infra.config import Config
from app.infra.kubernetes_helper import KubernetesHelper


@attr.s(auto_attribs=True)
class BaseSource(SourceRepository):
    config: Config
    source: EnforcementSource
    kubernetes_helper: KubernetesHelper
