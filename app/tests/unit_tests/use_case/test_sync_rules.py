from app.domain.cluster_group import ClusterGroup
from unittest import TestCase
from unittest.mock import MagicMock
from typing import List
from app.domain.use_case import SyncRulesUseCase
from app.domain.source_locator import SourceLocator
from app.domain.repositories import EnforcementRepository, ClusterRepository, ProjectRepository, SourceRepository
from app.domain.cluster_group_builder import ClusterGroupBuilder
from app.domain.entities import ClusterRule, Cluster, EnforcementSource


class SyncRulesTestCase(TestCase):
    def setUp(self) -> None:
        self.source_locator = SourceLocator()
        self.source_repository = SourceRepository()
        self.cluster_repository = ClusterRepository()
        self.project_repository = ProjectRepository()
        self.enforcement_repository = EnforcementRepository()

        self.cluster = Cluster(name='test', url='test', token='test', id='test')
        self.cluster_group = ClusterGroup(clusters=[self.cluster],
                                          cluster_repository=self.cluster_repository,
                                          project_repository=self.project_repository
                                          )
        self.cluster_group_builder = ClusterGroupBuilder(
            cluster_repository=self.cluster_repository,
            project_repository=self.project_repository
        )
        self.cluster_rule = ClusterRule(enforcements=[], source=EnforcementSource())


    def test_execute(self):
        self.source_locator.locate = MagicMock(return_value=self.source_repository)
        self.source_repository.get_clusters = MagicMock(return_value=[self.cluster])
        self.cluster_group_builder.build = MagicMock(return_value=self.cluster_group)
        self.enforcement_repository.list_installed_enforcements = MagicMock(return_value=[])

        sync_rules: SyncRulesUseCase = SyncRulesUseCase(
            source_locator=self.source_locator,
            enforcement_repository=self.enforcement_repository,
            cluster_group_builder=self.cluster_group_builder
        )

        cluster: List[Cluster] = sync_rules.execute(self.cluster_rule, self.cluster)

        self.assertEqual(1, len(cluster))