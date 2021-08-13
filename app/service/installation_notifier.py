from app.domain.triggers import TriggerService
from app.domain.entities import TriggerConfig
import requests


class InstallationNotifier(TriggerService):
    def send(self, trigger: TriggerConfig, payload: dict):
        response = requests.post(trigger.endpoint, json=payload, timeout=trigger.timeout)
        print(response.content)
        response.raise_for_status()

