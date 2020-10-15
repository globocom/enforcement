from injector import Injector
from typing import List

from app.di import ArgoModule, UseCaseModule
from app.controller import BaseController, ClusterGroupController


def register_controllers(controllers: List[BaseController]):
    for controller in controllers:
        controller.register()


injector = Injector([
    UseCaseModule(),
    ArgoModule(),
])

if __name__ == "main":
    all_controllers: List[BaseController] = [
        injector.get(ClusterGroupController),
    ]
    register_controllers(all_controllers)

