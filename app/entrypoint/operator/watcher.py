import attr
import threading
from queue import Queue
from kubernetes import watch
from kubernetes.client import CustomObjectsApi

from app.entrypoint.operator.cache import Cache
from app.entrypoint.operator.event import EventDetector, Event
from app.infra.config import Config


@attr.s(auto_attribs=True)
class Watcher:

    _event_queue: Queue
    _event_detector: EventDetector
    _cache: Cache
    _config: Config

    def __attrs_post_init__(self):
        self._watch_keys = {
            "group": self._config.api_group,
            "version": self._config.api_version,
            "namespace": self._config.current_namespace,
            "plural": "clusterrules",
        }

    def start(self):
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self) -> None:
        print("Iniciando watcher")
        api = CustomObjectsApi()

        for event_map in watch.Watch().stream(api.list_namespaced_custom_object, **self._watch_keys):
            event = self._event_detector.detect(event_map)
            self._event_queue.put(event)

        print("Finalizando watcher")


