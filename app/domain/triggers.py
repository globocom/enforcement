from app.domain.entities import TriggerConfig, TriggersConfig, Cluster, Enforcement
import attr
from typing import Callable


class InstallEvent:
    def __call__(self, cluster: Cluster, enforcement: Enforcement, success: bool = None) -> dict:
        event = {
            "cluster": {
                "name": cluster.name,
                "id": cluster.id,
                "url": cluster.url,
            },
            "enforcement": enforcement.dict(),
        }

        if not isinstance(success, type(None)):
            event["success"] = success

        return event


class TriggerService:
    def send(self, trigger: TriggerConfig, payload: dict):
        raise Exception('Not implemented')


@attr.s(auto_attribs=True)
class TriggerBase:
    _trigger_service: TriggerService

    def notify(self, trigger: TriggerConfig) -> Callable[[dict], None]:
        return lambda payload: \
            self._trigger_service.send(trigger=trigger, payload=payload) if trigger else None


@attr.s(auto_attribs=True)
class TriggerBuilder:
    _trigger_base: TriggerBase

    def build_before_install(self, triggers_config: TriggersConfig) \
            -> Callable[[Cluster, Enforcement], None]:
        def trigger(cluster: Cluster, enforcement: Enforcement):
            event = InstallEvent()
            sender = self._trigger_base.notify(trigger=triggers_config.beforeInstall)
            sender(event(cluster, enforcement))
        return TriggerBuilder.check_trigger(trigger, triggers_config)

    def build_after_install(self, triggers_config: TriggersConfig) \
            -> Callable[[Cluster, Enforcement], None]:
        def trigger(cluster: Cluster, enforcement: Enforcement):
            event = InstallEvent()
            sender = self._trigger_base.notify(trigger=triggers_config.afterInstall)
            sender(event(cluster, enforcement))
        return TriggerBuilder.check_trigger(trigger, triggers_config)

    @staticmethod
    def check_trigger(trigger: Callable[[Cluster, Enforcement], None],
                      triggers_config: TriggersConfig) \
            -> Callable[[Cluster, Enforcement], None]:
        return trigger if triggers_config else lambda c, e: None



