from typing import List

import attr

from app.domain.cluster_group import ClusterGroup
from app.domain.enforcement_installer import EnforcementInstaller
from app.domain.entities import Enforcement, TriggersConfig
from app.domain.repositories import EnforcementRepository
from app.domain.enforcement_dynamic_mapper import EnforcementDynamicMapper
from app.domain.triggers import TriggerBuilder


@attr.s(auto_attribs=True)
class EnforcementInstallerBuilder:
    _enforcement_repository: EnforcementRepository
    _enforcement_dynamic_mapper: EnforcementDynamicMapper
    _trigger_builder: TriggerBuilder

    def build(self, enforcements: List[Enforcement], cluster_group: ClusterGroup,
              triggers_config: TriggersConfig = None) -> EnforcementInstaller:

        before_install_trigger = self._trigger_builder.build_before_install(triggers_config)
        after_install_trigger = self._trigger_builder.build_after_install(triggers_config)

        return EnforcementInstaller(
            enforcements=enforcements,
            cluster_group=cluster_group,
            enforcement_repository=self._enforcement_repository,
            enforcement_dynamic_mapper=self._enforcement_dynamic_mapper,
            before_install_trigger=before_install_trigger,
            after_install_trigger=after_install_trigger,
        )
