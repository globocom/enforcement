from injector import Injector
from typing import List

from app.config import DataModule, UseCaseModule
from app.entrypoint.operator import BaseController, ClusterRuleController


def register_controllers(controllers: List[BaseController]):
    for controller in controllers:
        controller.register()


injector = Injector([
    UseCaseModule(),
    DataModule(),
])

if __name__ == "main":
    all_controllers: List[BaseController] = [
        injector.get(ClusterRuleController),
    ]
    register_controllers(all_controllers)

