from unittest import TestCase
from unittest.mock import patch, MagicMock

from app.domain.cluster_group import ClusterGroup
from app.domain.enforcement_installer import EnforcementInstaller
from app.domain.entities import Enforcement, Cluster
from app.domain.repositories import EnforcementRepository, ClusterRepository, ProjectRepository
from app.domain.enforcement_dynamic_mapper import EnforcementDynamicMapper


class enforcementInstallerTestCase(TestCase):
    def setUp(self) -> None:
        self.enforcement_repository = EnforcementRepository()
        self.enforcement_dynamic_mapper = EnforcementDynamicMapper()
        self.enforcement = Enforcement(name='test', repo='somewhere', labels={'cluster_name': 'test'})
        self.cluster_repository = ClusterRepository()
        self.project_repository = ProjectRepository()
        self.cluster = Cluster(name='test', url='test',
                               token='test', id='test')
        self.cluster_group = ClusterGroup(
            clusters=[self.cluster],
            cluster_repository=self.cluster_repository,
            project_repository=self.project_repository
        )

    @patch('app.domain.repositories.EnforcementRepository.create_enforcement')
    @patch('app.domain.repositories.EnforcementRepository.list_installed_enforcements')
    def test_install_create_repository(self, mock_list_installed_enforcements, mock_create_enforcement) -> None:
        enforcement_installer = EnforcementInstaller(
            enforcements=[self.enforcement],
            cluster_group=self.cluster_group,
            enforcement_repository=self.enforcement_repository,
            enforcement_dynamic_mapper=EnforcementDynamicMapper(),
            before_install_trigger=lambda cluster, enforcement: None,
            after_install_trigger=lambda cluster, enforcement: None
        )

        enforcement_installer.install()

        self.assertTrue(mock_list_installed_enforcements.called)
        self.assertTrue(mock_create_enforcement.called)
        self.assertEqual(
            mock_create_enforcement.call_args[0][0], self.enforcement.name)
        self.assertEqual(
            mock_create_enforcement.call_args[0][1], enforcement_installer._make_enforcement_name(self.cluster, self.enforcement))
        self.assertEqual(
            mock_create_enforcement.call_args[0][2], self.enforcement)

    @patch('app.domain.repositories.EnforcementRepository.update_enforcement')
    @patch('app.domain.repositories.EnforcementRepository.create_enforcement')
    def test_install_update_repository(self, mock_update_enforcement, mock_create_enforcement) -> None:
        enforcement = Enforcement(name='test-test', repo='somewhere', labels={'cluster_name': 'test'})

        repository = EnforcementRepository()
        repository.list_installed_enforcements = MagicMock(return_value=[enforcement])

        enforcement_installer = EnforcementInstaller(
            enforcements=[self.enforcement],
            cluster_group=self.cluster_group,
            enforcement_repository=repository,
            enforcement_dynamic_mapper=EnforcementDynamicMapper(),
            before_install_trigger=lambda cluster, enforcement: None,
            after_install_trigger=lambda cluster, enforcement: None
        )

        enforcements = enforcement_installer.install()

        self.assertListEqual([], enforcements)

    @patch('app.domain.repositories.EnforcementRepository.remove_enforcement')
    @patch('app.domain.repositories.EnforcementRepository.list_installed_enforcements')
    def test_uninstall(self, mock_list_installed_enforcements, mock_remove_enforcement) -> None:
        enforcement = Enforcement(name='test-test', repo='somewhere')
        mock_list_installed_enforcements.return_value = [enforcement]

        enforcement_installer = EnforcementInstaller(
            enforcements=[self.enforcement],
            cluster_group=self.cluster_group,
            enforcement_repository=self.enforcement_repository,
            enforcement_dynamic_mapper=EnforcementDynamicMapper(),
            before_install_trigger=lambda cluster, enforcement: None,
            after_install_trigger=lambda cluster, enforcement: None
        )

        enforcement_installer.uninstall()

        self.assertTrue(mock_list_installed_enforcements.called)
        self.assertEqual(
            mock_list_installed_enforcements.call_args[1]['cluster_name'], self.cluster.name)
        self.assertTrue(mock_remove_enforcement.called)
        self.assertEqual(
            mock_remove_enforcement.call_args[0][0], enforcement_installer._make_enforcement_name(self.cluster, self.enforcement))
