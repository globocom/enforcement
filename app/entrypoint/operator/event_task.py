import attr
import time

from app.entrypoint.operator.event import Event, Type
from app.entrypoint.operator.cache import Cache, CacheItem
from app.entrypoint.operator.controller import ClusterRuleController


class EventTask:

    def __init__(self, event: Event, controller: ClusterRuleController, cache: Cache):
        self._event = event
        self._controller = controller
        self._cache = cache

    def __call__(self, *args, **kwargs):
        raise Exception("Not Implemented")


class CreateEventTask(EventTask):

    MAX_ERRORS: int = 3
    RETRY_DELAY: int = 4

    def __call__(self, *args, **kwargs):
        cache_item = CacheItem(self._event.cluster_rule)
        self._cache.insert(cache_item)

        cache_item.lock()

        for _ in range(CreateEventTask.MAX_ERRORS):

            try:
                self._controller.create(cache_item.name, cache_item.spec)
                break
            except Exception:
                time.sleep(CreateEventTask.RETRY_DELAY)

        cache_item.free()


@attr.s(auto_attribs=True)
class EventTaskFactory:
    _cache: Cache
    _controller: ClusterRuleController

    def __attrs_post_init__(self):
        self._tasks = {
            Type.CREATE: CreateEventTask,
        }

    def create_task(self, event: Event) -> EventTask:

        if event.type == Type.UPDATE:
            return None

        task_class = self._tasks[event.type]
        task: EventTask = task_class(
            event=event,
            cache=self._cache,
            controller=self._controller,
        )

        return task
