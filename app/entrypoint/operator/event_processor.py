import attr
import threading
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor


from app.entrypoint.operator.event import Event
from app.entrypoint.operator.event_task import EventTaskFactory


@attr.s(auto_attribs=True)
class EventProcessor:
    _event_queue: Queue
    _event_task_factory: EventTaskFactory

    def __attrs_post_init__(self):
        self._stop_event = threading.Event()
        self._executor = ThreadPoolExecutor(max_workers=10)

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

                task = self._event_task_factory.create_task(event)

                if task:
                    self._executor.submit(task)

            except Empty:
                continue

        print("Finalizando event processor")
