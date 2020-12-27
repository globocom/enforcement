import attr
from typing import List

from app.domain.repositories import EnforcementRepository
from app.domain.entities import Cluster, Enforcement
from app.domain.cluster_group_builder import ClusterGroupBuilder
from app.domain.enforcement_installer import EnforcementInstaller
from app.domain.enforcement_change_detector import EnforcementChangeDetector

from app.domain.use_case.responses import UpdateRulesResponse


@attr.s(auto_attribs=True)
class UpdateRulesUseCase:
    _enforcement_repository: EnforcementRepository
    _cluster_group_builder: ClusterGroupBuilder

    def execute(self, clusters: List[Cluster], old_enforcements: List[Enforcement],
                new_enforcements: List[Enforcement]) -> UpdateRulesResponse:

        if not clusters:
            return UpdateRulesResponse(install_errors=[], update_errors=[])

        change_detector = EnforcementChangeDetector(
            new_enforcements_list=new_enforcements,
            old_enforcements_list=old_enforcements
        )

        self._uninstall_removed_enforcements(change_detector, clusters)
        add_errors = self._install_added_enforcements(change_detector, clusters)
        update_errors = self._update_change_enforcements(change_detector, clusters)

        return UpdateRulesResponse(
            install_errors=add_errors,
            update_errors=update_errors
        )

    def _update_change_enforcements(self, change_detector: EnforcementChangeDetector,
                                    clusters: List[Cluster]) -> List[Enforcement]:
        change_enforcements = change_detector.detect_change_enforcements()

        if not change_enforcements:
            return []

        cluster_group_change_enfocement = self._cluster_group_builder.build(
            clusters=clusters
        )

        enforcement_installer = EnforcementInstaller(
            enforcement_repository=self._enforcement_repository,
            cluster_group=cluster_group_change_enfocement,
            enforcements=change_enforcements
        )

        return enforcement_installer.install()

    def _install_added_enforcements(self, change_detector: EnforcementChangeDetector,
                                    clusters: List[Cluster]) -> List[Enforcement]:
        added_enforcements = change_detector.detect_new_enforcements()

        if not added_enforcements:
            return []

        cluster_group_remove_enfocement = self._cluster_group_builder.build(
            clusters=clusters
        )

        enforcement_installer = EnforcementInstaller(
            enforcement_repository=self._enforcement_repository,
            cluster_group=cluster_group_remove_enfocement,
            enforcements=added_enforcements
        )

        return enforcement_installer.install()

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

