from dataclasses import dataclass, field
from typing import Optional, List

from model.enforcement import Enforcement
from data import EnforcementRepository


@dataclass
class Cluster:
    name: str
    token: str
    url: str
    _enforcement_repository: EnforcementRepository
    _enforcements: List[Enforcement] = field(default=[], init=False)
    id: Optional[str] = field(default=None)

    def apply_all_enforcements(self):
        for enforcement in self._enforcements:
            self._enforcement_repository.create_enforcement(self.name, enforcement)

    def remove_all_enforcements(self):
        pass












