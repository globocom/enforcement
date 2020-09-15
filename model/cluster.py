from dataclasses import dataclass
from typing import Optional
from model.enforcement import EnforcementOfCluster


@dataclass
class Cluster:
    name: str
    token: str
    url: str
    id: Optional[str] = None

    def __post_init__(self):
        self._enforcements = EnforcementOfCluster()

    @property
    def enforcements(self):
        return self._enforcements








