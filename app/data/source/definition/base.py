import attr

from app.domain.entities import EnforcementSource
from app.domain.repositories import SourceRepository
from app.infra.config import Config


@attr.s(auto_attribs=True)
class BaseSource(SourceRepository):
    config: Config
    source: EnforcementSource
