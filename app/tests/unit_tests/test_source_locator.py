from unittest import TestCase
from unittest.mock import MagicMock

from app.domain.entities import EnforcementSource, RancherSource
from app.domain.repositories import SourceRepository
from app.domain.source_locator import SourceLocator


class SourceLocatorTestCase(TestCase):
    def setUp(self) -> None:
        self.source_repository: SourceRepository = SourceRepository()
        self.rancher_source: RancherSource = RancherSource()
        self.enforcement_source: EnforcementSource = EnforcementSource(
            rancher=self.rancher_source
        )

    def test_locate(self) -> None:
        source_locator: SourceLocator = SourceLocator()
        source_locator.locate = MagicMock(return_value=self.source_repository)

        source_repository: SourceRepository = source_locator.locate(
            self.enforcement_source)

        self.assertTrue(type(source_repository) is SourceRepository)
