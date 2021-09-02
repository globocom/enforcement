from unittest import TestCase
from unittest.mock import MagicMock

from app.domain.cluster_group import ClusterGroup
from app.domain.enforcement_installer import EnforcementInstaller
from app.domain.enforcement_installer_builder import EnforcementInstallerBuilder
from app.domain.entities import Enforcement, Cluster
from app.domain.repositories import EnforcementRepository, ClusterRepository, ProjectRepository
from app.domain.enforcement_dynamic_mapper import EnforcementDynamicMapper


class EnforcementInstallerBuilderTestCase(TestCase):
    def setUp(self) -> None:
        self.dynamic_mapper = EnforcementDynamicMapper()
        self.enforcement_repository = EnforcementRepository()
        self.enforcement = Enforcement(name='test', repo='somewhere')
        self.cluster_repository = ClusterRepository()
        self.project_repository = ProjectRepository()
        self.cluster = Cluster(name='test', url='test',
                               token='test', id='test')
        self.cluster_group = ClusterGroup(
            clusters=[self.cluster],
            cluster_repository=self.cluster_repository,
            project_repository=self.project_repository
        )

        self.trigger_function = lambda enf, cluster: None

        self.enforcement_installer = EnforcementInstaller(
            enforcements=[self.enforcement],
            cluster_group=self.cluster_group,
            enforcement_repository=self.enforcement_repository,
            enforcement_dynamic_mapper=self.dynamic_mapper,
        )

    def test_build(self) -> None:
        trigger_builder = MagicMock()
        trigger_builder.build_before_install = MagicMock(return_value=self.trigger_function)
        trigger_builder.build_after_install = MagicMock(return_value=self.trigger_function)

        enforcement_installer_builder = EnforcementInstallerBuilder(
            enforcement_repository=self.enforcement_repository,
            enforcement_dynamic_mapper=self.dynamic_mapper,
            trigger_builder=trigger_builder,
        )

        enforcement_installer = enforcement_installer_builder.build(
            enforcements=[self.enforcement],
            cluster_group=self.cluster_group,
        )

        self.assertEqual(self.enforcement_installer, enforcement_installer)

    def test_build_throws_exception_required_argument(self) -> None:
        trigger_builder = MagicMock()
        trigger_builder.build_before_install = MagicMock(return_value=self.trigger_function)
        trigger_builder.build_after_install = MagicMock(return_value=self.trigger_function)

        enforcement_installer_builder = EnforcementInstallerBuilder(
            enforcement_repository=self.enforcement_repository,
            enforcement_dynamic_mapper=self.dynamic_mapper,
            trigger_builder=trigger_builder
        )
        
        with self.assertRaises(Exception) as context:
            enforcement_installer_builder.build()

        self.assertTrue('required positional argument' in str(context.exception))