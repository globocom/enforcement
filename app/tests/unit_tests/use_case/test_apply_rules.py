from unittest import TestCase
from unittest.mock import Mock
from typing import List
from app.domain.use_case import ApplyRulesUseCase
from app.domain.source_locator import SourceLocator
from app.domain.repositories import EnforcementRepository, ClusterRepository, ProjectRepository, SourceRepository
from app.domain.cluster_group_builder import ClusterGroupBuilder
from app.domain.entities import ClusterRule, Cluster, EnforcementSource


class ApplyRulesTestCase(TestCase):
    def setUp(self) -> None:
        self.source_locator = SourceLocator()
        self.enforcement_repository = EnforcementRepository()
        self.cluster_group_builder = ClusterGroupBuilder(
            cluster_repository=ClusterRepository(),
            project_repository=ProjectRepository()
        )

    
    def test_execute(self):
        apply_rules: ApplyRulesUseCase = ApplyRulesUseCase(
            source_locator = self.source_locator,
            enforcement_repository = self.enforcement_repository,
            cluster_group_builder = self.cluster_group_builder
        )

        
        cluster_rule = ClusterRule(enforcements=[], source=EnforcementSource())
        cluster: List[Cluster] = apply_rules.execute(cluster_rule)

        self.assertEqual(1, len(cluster))
