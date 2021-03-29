from injector import Injector
import signal

from app.config import DataModule, UseCaseModule,  DomainModule, InfraModule, OperatorModule, \
    OperatorControllerModule
from app.entrypoint.operator import OperatorEngine


injector = Injector([
    UseCaseModule(),
    DataModule(),
    DomainModule(),
    InfraModule(),
    OperatorModule(),
    OperatorControllerModule(),
])

if __name__ == "__main__":
    engine: OperatorEngine = injector.get(OperatorEngine)
    signal.signal(signal.SIGINT, engine.stop)
    engine.start()
