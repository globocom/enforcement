from app.domain.entities import EnforcementSource

class SourceUtils:

    @staticmethod
    def get_source_name(source: EnforcementSource) -> str:
        return list(source.__dict__.keys())[0]