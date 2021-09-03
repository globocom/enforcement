from app.domain.triggers import TriggerService
from app.domain.entities import TriggerConfig
import requests
from requests.exceptions import Timeout


class InstallationNotifier(TriggerService):
    def send(self, trigger: TriggerConfig, payload: dict) -> bool:
        try:
            response = requests.post(trigger.endpoint, json=payload, timeout=trigger.timeout)
            return 200 < response.status_code < 300
        except Timeout:
            return False

