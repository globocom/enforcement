import attr
import threading
import time
from queue import Queue

from app.entrypoint.operator.cache import Cache


@attr.s(auto_attribs=True)
class Watcher:

    _event_queue: Queue
    _cache: Cache

    def start(self):
        thread = threading.Thread(target=self._run)
        thread.start()

    def _run(self) -> None:
        print("Iniciando watcher")
        print(self._event_queue)
        time.sleep(5)
        print("Finalizando watcher")

