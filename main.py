from injector import Injector
from typing import List

from di.argo_module import ArgoModule

from controller.base_controller import BaseController
from controller.cluster_group import ClusterGroupController


def register_controllers(controllers: List[BaseController]):
    for controller in controllers:
        controller.register()


injector = Injector([
    ArgoModule()
])

if __name__ == "main":
    all_controllers: List[BaseController] = [
        injector.get(ClusterGroupController),
    ]
    register_controllers(all_controllers)

