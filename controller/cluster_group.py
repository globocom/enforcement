from injector import inject
import kopf
from controller.base_controller import BaseController


class ClusterGroupController(BaseController):
    @inject
    def __init__(self):
        pass

    def create(self, spec: dict, name: str, namespace: str, body: dict, logger, **kwargs):
        logger.info("Invoke create controller")
        logger.info(f"Object created %s", body)

    def register(self):
        self.register_method(kopf.on.create, self.create, 'clustergroups')

