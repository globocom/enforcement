import attr
import threading
from queue import Queue, Empty

from app.entrypoint.operator.cache import Cache
from app.entrypoint.operator.event import Event


@attr.s(auto_attribs=True)
class EventProcessor:
    _event_queue: Queue
    _cache: Cache

    def __attrs_post_init__(self):
        self._stop_event = threading.Event()

    def start(self):

        thread = threading.Thread(target=self._run)
        thread.start()

    def stop(self):
        self._stop_event.set()

    def _run(self):
        print("Inicializando event processor")

        while not self._stop_event.is_set() or not self._event_queue.empty():
            try:
                event: Event = self._event_queue.get(timeout=5)
                evt = event.cluster_rule

                print("Event: %s %s" % (evt["kind"], evt["metadata"]["name"]))
                print(event.type)

            except Empty:
                continue

        print("Finalizando event processor")
