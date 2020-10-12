from injector import inject
import kopf
from controller.base_controller import BaseController
from data.datasource.rancher import RancherRepository


class ClusterGroupController(BaseController):

    KIND: str = 'clustergroups'

    @inject
    def __init__(self, rancher_repository: RancherRepository):
        self._rancher_repository = rancher_repository

    def create(self, spec: dict, name: str, namespace: str, body: dict, logger, **kwargs):
        logger.info("Invoke create controller")
        logger.info(f"Object created %s", body)

    def register(self):
        self.register_method(kopf.on.create, self.create, ClusterGroupController.KIND)

