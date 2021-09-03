from injector import Module, provider, singleton
from app.domain.triggers import TriggerService
from app.service.installation_notifier import InstallationNotifier


class ServiceModule(Module):
    @provider
    @singleton
    def provide_installation_notifier(self) -> TriggerService:
        return InstallationNotifier()


