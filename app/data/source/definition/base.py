import attr

from app.domain.repositories import SourceRepository
from app.domain.entities import EnforcementSource
from app.infra.config import Config


@attr.s(auto_attribs=True)
class BaseSource(SourceRepository):
    config: Config
    source: EnforcementSource


