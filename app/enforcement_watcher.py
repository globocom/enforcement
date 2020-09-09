from service.rancher import RancherService


class EnforcementWatcher:
    def __init__(self, rancher_service: RancherService):
        self._rancher_service = rancher_service

    def run(self):
        print(self._rancher_service.get_clusters())
