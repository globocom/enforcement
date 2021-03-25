import attr
import threading
import time
from queue import Queue

from app.entrypoint.operator.cache import Cache


@attr.s(auto_attribs=True)
class EventProcessor:
    _event_queue: Queue
    _cache: Cache

    def start(self):
        thread = threading.Thread(target=self._run)
        thread.start()

    def _run(self):
        print("Inicializando event processor")
        time.sleep(3)
        print("Finalizando event processor")
