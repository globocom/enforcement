import attr
from typing import List

from app.data.repository.enforcement import EnforcementRepository
from app.model.entities import Cluster, Enforcement


@attr.s(auto_attribs=True)
class ApplyEnforcementsUseCase:
    _enforcement_repository: EnforcementRepository

    def execute(self, clusters: List[Cluster], enforcements: List[Enforcement]):
        for cluster in clusters:
            installed_enforcements = self._enforcement_repository.list_installed_enforcements(cluster_name=cluster.name)
            installed_enforcements_names = self._get_enforcements_name(installed_enforcements)
            for enforcement in enforcements:
                if enforcement.name not in installed_enforcements_names:
                    self._enforcement_repository.create_enforcement(cluster.name, enforcement)

    @classmethod
    def _get_enforcements_name(cls, enforcements: List[Enforcement]):
        return {enforcement.name: enforcement for enforcement in enforcements}
