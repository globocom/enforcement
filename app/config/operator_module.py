from injector import Module, provider, singleton
from queue import Queue

from app.entrypoint.operator.watcher import Watcher
from app.entrypoint.operator.engine import OperatorEngine
from app.entrypoint.operator.event_processor import EventProcessor
from app.entrypoint.operator.cache import Cache
from app.infra.config import Config


class OperatorModule(Module):

    @provider
    @singleton
    def provide_event_watcher_queue(self) -> Queue:
        return Queue(maxsize=10)

    @provider
    @singleton
    def provide_watcher(self, event_queue: Queue, cache: Cache, cfg: Config) -> Watcher:
        return Watcher(event_queue=event_queue, cache=cache, config=cfg)

    @provider
    @singleton
    def provide_operator_engine(self, watcher: Watcher, event_processor: EventProcessor) -> OperatorEngine:
        return OperatorEngine(watcher=watcher, event_processor=event_processor)

    @provider
    @singleton
    def provide_event_processor(self, event_queue: Queue, cache: Cache) -> EventProcessor:
        return EventProcessor(event_queue=event_queue, cache=cache)

    @provider
    @singleton
    def provide_cache(self) -> Cache:
        return Cache()
