from app.domain.trigger_service import TriggerService
from app.domain.entities import Trigger
import requests


class InstallationNotifier(TriggerService):
    def send(self, trigger: Trigger, payload: dict):
        response = requests.post(trigger.endpoint, json=payload, timeout=trigger.timeout)
        print(response.content)
        response.raise_for_status()

