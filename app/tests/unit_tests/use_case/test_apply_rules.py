from app.data.argo import project
from app.domain.cluster_group import ClusterGroup
from unittest import TestCase
from unittest.mock import MagicMock
from typing import List
from app.domain.use_case import ApplyRulesUseCase
from app.domain.source_locator import SourceLocator
from app.domain.repositories import EnforcementRepository, ClusterRepository, ProjectRepository, SourceRepository
from app.domain.cluster_group_builder import ClusterGroupBuilder
from app.domain.entities import ClusterRule, Cluster, EnforcementSource


class ApplyRulesTestCase(TestCase):
    def setUp(self) -> None:
        self.source_locator = SourceLocator()
        self.source_repository = SourceRepository()
        self.cluster_repository = ClusterRepository()
        self.project_repository = ProjectRepository()

        self.cluster = Cluster(name='test', url='test', token='test', id='test')
        self.cluster_group = ClusterGroup(clusters=[self.cluster],
                                          cluster_repository=self.cluster_repository,
                                          project_repository=self.project_repository
                                          )
        self.cluster_group_builder = ClusterGroupBuilder(
            cluster_repository=self.cluster_repository,
            project_repository=self.project_repository
        )

    def test_execute_with_zero_clusters(self):
        self.source_repository.get_clusters = MagicMock(return_value=[])
        self.source_locator.locate = MagicMock(return_value=self.source_repository)

        apply_rules: ApplyRulesUseCase = ApplyRulesUseCase(
            source_locator=self.source_locator,
            enforcement_repository=EnforcementRepository(),
            cluster_group_builder=self.cluster_group_builder
        )

        cluster: List[Cluster] = apply_rules.execute(ClusterRule(enforcements=[], source=EnforcementSource()))

        self.assertEqual(0, len(cluster))

    def test_execute_with_clusters(self):
        enforcement_repository = EnforcementRepository()

        self.source_locator.locate = MagicMock(return_value=self.source_repository)
        self.source_repository.get_clusters = MagicMock(return_value=[self.cluster])
        self.cluster_group_builder.build = MagicMock(return_value=self.cluster_group)
        self.cluster_group.register = MagicMock(return_value=None)
        enforcement_repository.list_installed_enforcements = MagicMock(return_value=[])

        apply_rules: ApplyRulesUseCase = ApplyRulesUseCase(
            source_locator=self.source_locator,
            enforcement_repository=enforcement_repository,
            cluster_group_builder=self.cluster_group_builder
        )

        cluster: List[Cluster] = apply_rules.execute(ClusterRule(enforcements=[], source=EnforcementSource()))

        self.assertEqual(1, len(cluster))
