from dataclasses import dataclass, field
from typing import Optional, List, Callable

from model.enforcement import Enforcement
from data.repository.enforcement import EnforcementRepository


@dataclass
class Cluster:
    name: str
    token: str
    url: str
    _enforcement_repository: EnforcementRepository
    _enforcements: List[Enforcement] = field(default_factory=list, init=False)
    _default_enforcement_factory: Callable[[], Enforcement]
    id: Optional[str] = field(default=None)

    def __post_init__(self):
        self._detect_new_enforcements()

    def apply_all_enforcements(self):
        for enforcement in self._enforcements:
            self._enforcement_repository.create_enforcement(enforcement)

    def remove_all_enforcements(self):
        installed_enforcements = self._enforcement_repository.list_installed_enforcements(
            cluster=self.name
        )
        for enforcement in installed_enforcements:
            self._enforcement_repository.remove_enforcement(enforcement)

    def _detect_new_enforcements(self):
        self._enforcements.append(self._default_enforcement_factory())













