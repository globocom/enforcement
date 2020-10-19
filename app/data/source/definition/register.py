from typing import Dict, Callable
from app.data.source.rancher import RancherDatasource


class SourceRegister:
    sources: Dict[str, Callable] = {
        'rancher': RancherDatasource
    }

    @classmethod
    def find_source(cls, source_name: str) -> Callable:
        return cls.sources.get(source_name)


