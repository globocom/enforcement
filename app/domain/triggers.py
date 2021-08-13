from app.domain.entities import TriggerConfig, TriggersConfig
import attr
from typing import Callable


class TriggerService:
    def send(self, trigger: TriggerConfig, payload: dict):
        raise Exception('Not implemented')


@attr.s(auto_attribs=True)
class TriggerBase:
    _trigger_service: TriggerService

    def notify(self, trigger: TriggerConfig) -> Callable:
        return lambda payload: \
            self._trigger_service.send(trigger=trigger, payload=payload) if trigger else None


@attr.s(auto_attribs=True)
class TriggerBuilder:
    _trigger_base: TriggerBase

    def build_before_install(self, triggers_config: TriggersConfig) -> Callable:
        return self._trigger_base.notify(trigger=triggers_config.beforeInstall)

    def build_after_install(self, triggers_config: TriggersConfig) -> Callable:
        return self._trigger_base.notify(trigger=triggers_config.afterInstall)

