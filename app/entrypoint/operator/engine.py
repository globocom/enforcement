import attr
import threading
from signal import Signals
from types import FrameType
from app.entrypoint.operator.watcher import Watcher
from app.entrypoint.operator.event_processor import EventProcessor


@attr.s(auto_attribs=True)
class OperatorEngine:

    _watcher: Watcher
    _event_processor: EventProcessor

    def __attrs_post_init__(self):
        self._stop_event = threading.Event()

    def start(self):
        print("Iniciando operator engine")
        self._watcher.start()
        self._event_processor.start()
        print("Finalizando operator engine")

    def stop(self, signal: Signals, frame: FrameType):
        self._event_processor.stop()

