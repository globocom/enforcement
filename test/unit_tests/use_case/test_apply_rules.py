from unittest import TestCase
from unittest.mock import MagicMock, patch

from app.domain.cluster_group import ClusterGroup
from app.domain.cluster_group_builder import ClusterGroupBuilder
from app.domain.enforcement_installer import EnforcementInstaller
from app.domain.enforcement_installer_builder import EnforcementInstallerBuilder
from app.domain.entities import ClusterRule, Cluster, EnforcementSource, Enforcement
from app.domain.repositories import EnforcementRepository, ClusterRepository, ProjectRepository, SourceRepository
from app.domain.source_locator import SourceLocator
from app.domain.use_case import ApplyRulesUseCase
from app.domain.enforcement_dynamic_mapper import EnforcementDynamicMapper


class ApplyRulesTestCase(TestCase):
    def setUp(self) -> None:
        self.dynamic_mapper = EnforcementDynamicMapper()
        self.source_locator = SourceLocator()
        self.source_repository = SourceRepository()
        self.cluster_repository = ClusterRepository()
        self.project_repository = ProjectRepository()
        self.enforcement_repository = EnforcementRepository()
        self.enforcement = Enforcement(name='test', repo='somewhere')

        self.cluster = Cluster(name='test', url='test',
                               token='test', id='test')
        self.cluster_group = ClusterGroup(clusters=[self.cluster],
                                          cluster_repository=self.cluster_repository,
                                          project_repository=self.project_repository
                                          )

        self.cluster_group_builder = ClusterGroupBuilder(
            cluster_repository=self.cluster_repository,
            project_repository=self.project_repository
        )

        self.cluster_rule = ClusterRule(
            enforcements=[], source=EnforcementSource())

        trigger_builder = MagicMock()
        trigger_builder.build_before_install = MagicMock(return_value=lambda enf, cluster: None)
        trigger_builder.build_after_install = MagicMock(return_value=lambda enf, cluster: None)

        self.enforcement_installer_builder = EnforcementInstallerBuilder(
            enforcement_repository=self.enforcement_repository,
            enforcement_dynamic_mapper=EnforcementDynamicMapper(),
            trigger_builder=trigger_builder,
        )
        self.enforcement_installer = EnforcementInstaller(
            enforcements=[self.enforcement],
            cluster_group=self.cluster_group,
            enforcement_repository=self.enforcement_repository,
            enforcement_dynamic_mapper=self.dynamic_mapper,
            before_install_trigger=lambda a1, a2: None,
            after_install_trigger=lambda a1, a2: None,
        )

    def test_execute(self) -> None:
        self.source_locator.locate = MagicMock(
            return_value=self.source_repository)
        self.source_repository.get_clusters = MagicMock(
            return_value=[self.cluster])
        self.cluster_group_builder.build = MagicMock(
            return_value=self.cluster_group)
        self.cluster_group.register = MagicMock(return_value=None)
        self.enforcement_installer_builder.build = MagicMock(
            return_value=self.enforcement_installer)
        self.enforcement_installer.install = MagicMock(retun_value=None)

        apply_rules = ApplyRulesUseCase(
            source_locator=self.source_locator,
            cluster_group_builder=self.cluster_group_builder,
            enforcement_installer_builder=self.enforcement_installer_builder,
        )

        response = apply_rules.execute(self.cluster_rule)

        self.assertEqual(1, len(response.clusters))
        self.assertEqual(0, len(response.install_errors))
        self.assertTrue(self.source_locator.locate.called)
        self.assertTrue(self.source_repository.get_clusters.called)
        self.assertTrue(self.cluster_group_builder.build.called)
        self.assertTrue(self.cluster_group.register.called)
        self.assertTrue(self.enforcement_installer_builder.build.called)
        self.assertTrue(self.enforcement_installer.install.called)
