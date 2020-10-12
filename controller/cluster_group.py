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

    # noinspection PyTypeChecker
    def register(self):
        create_decorate = kopf.on.create('enforcement.globo.com', 'v1beta1', 'clustergroups')
        create_decorate(self.create)

