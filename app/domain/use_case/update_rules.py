import attr
from typing import List

from app.domain.repositories import EnforcementRepository
from app.domain.entities import Cluster, Enforcement
from app.domain.cluster_group_builder import ClusterGroupBuilder
from app.domain.enforcement_installer import EnforcementInstaller
from app.domain.enforcement_change_detector import EnforcementChangeDetector


@attr.s(auto_attribs=True)
class UpdateRulesUseCase:
    _enforcement_repository: EnforcementRepository
    _cluster_group_builder: ClusterGroupBuilder

    def execute(self, clusters: List[Cluster], old_enforcements: List[Enforcement],
                new_enforcements: List[Enforcement]):

        change_detector = EnforcementChangeDetector(
            new_enforcements_list=new_enforcements,
            old_enforcements_list=old_enforcements
        )

        self._uninstall_removed_enforcements(change_detector, clusters)
        self._install_added_enforcements(change_detector, clusters)
        self._update_change_enforcements(change_detector, clusters)

    def _update_change_enforcements(self, change_detector: EnforcementChangeDetector, clusters: List[Cluster]):
        change_enforcements = change_detector.detect_change_enforcements()

        if not change_enforcements:
            return

        cluster_group_change_enfocement = self._cluster_group_builder.build(
            clusters=clusters
        )

        enforcement_installer = EnforcementInstaller(
            enforcement_repository=self._enforcement_repository,
            cluster_group=cluster_group_change_enfocement,
            enforcements=change_enforcements
        )

        enforcement_installer.install()

    def _install_added_enforcements(self, change_detector: EnforcementChangeDetector, clusters: List[Cluster]):
        added_enforcements = change_detector.detect_new_enforcements()

        if not added_enforcements:
            return

        cluster_group_remove_enfocement = self._cluster_group_builder.build(
            clusters=clusters
        )

        enforcement_installer = EnforcementInstaller(
            enforcement_repository=self._enforcement_repository,
            cluster_group=cluster_group_remove_enfocement,
            enforcements=added_enforcements
        )

        enforcement_installer.install()

    def _uninstall_removed_enforcements(self, change_detector: EnforcementChangeDetector, clusters: List[Cluster]):
        removed_enforcements = change_detector.detect_removed_enforcements()

        if not removed_enforcements:
            return

        cluster_group_remove_enfocement = self._cluster_group_builder.build(
            clusters=clusters
        )

        enforcement_installer = EnforcementInstaller(
            enforcement_repository=self._enforcement_repository,
            cluster_group=cluster_group_remove_enfocement,
            enforcements=removed_enforcements
        )

        enforcement_installer.uninstall()

