from typing import List

import attr
from argocd_client import ApiException

from app.domain.cluster_group import ClusterGroup
from app.domain.entities import Enforcement, Cluster
from app.domain.repositories import EnforcementRepository
from app.domain.exceptions import EnforcementInvalidException


@attr.s(auto_attribs=True)
class EnforcementInstaller:
    _enforcements: List[Enforcement]
    _cluster_group: ClusterGroup
    _enforcement_repository: EnforcementRepository

    def install(self) -> List[Enforcement]:

        enforcements_error: List[Enforcement] = []

        for cluster in self._cluster_group.clusters:
            installed_enforcements = self._enforcement_repository.list_installed_enforcements(cluster_name=cluster.name)
            installed_enforcements_names = self._get_enforcements_name(installed_enforcements)
            for enforcement in self._enforcements:
                instance_name = self._make_enforcement_name(cluster, enforcement)
                try:
                    if instance_name not in installed_enforcements_names:
                        self._enforcement_repository.create_enforcement(cluster.name, instance_name, enforcement)
                    else:
                        self._enforcement_repository.update_enforcement(cluster.name, instance_name, enforcement)
                except EnforcementInvalidException:
                    enforcements_error.append(enforcement)

        return enforcements_error

    def uninstall(self):
        for cluster in self._cluster_group.clusters:
            installed_enforcements = self._enforcement_repository.list_installed_enforcements(cluster_name=cluster.name)
            installed_enforcements_names = self._get_enforcements_name(installed_enforcements)
            for enforcement in self._enforcements:
                instance_name = self._make_enforcement_name(cluster, enforcement)
                if instance_name in installed_enforcements_names:
                    self._remove_enforcement(instance_name)

    def uninstall_project_apps(self):
        for cluster in self._cluster_group.clusters:
            installed_enforcements = self._enforcement_repository.list_project_apps(project_name=cluster.name)
            for enforcement in installed_enforcements:
                self._remove_enforcement(enforcement.name)

    def _remove_enforcement(self, enforcement_name):
        try:
            self._enforcement_repository.remove_enforcement(enforcement_name)
        except ApiException as e:
            if e.status != 404:
                raise e

    @classmethod
    def _get_enforcements_name(cls, enforcements: List[Enforcement]):
        return {enforcement.name: enforcement for enforcement in enforcements}

    @classmethod
    def _make_enforcement_name(cls, cluster: Cluster, enforcement: Enforcement) -> str:
        return f"{cluster.name}-{enforcement.name}"

    @classmethod
    def _make_enforcement_by_cluster(cls, enforcements) -> dict:
        by_cluster: dict = {}
        for enforcement in enforcements:
            cluster_name = enforcement.labels.get("cluster_name")
            if not cluster_name:
                continue
            by_cluster[cluster_name] = by_cluster.get(cluster_name, []) + [enforcement]
        return by_cluster

