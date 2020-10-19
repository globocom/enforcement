from app.domain.repositories import SourceRepository
from app.domain.entities import EnforcementSource


class SourceLocator:
    def locate(self, source: EnforcementSource) -> SourceRepository:
        pass
