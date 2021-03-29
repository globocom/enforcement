import attr
import threading
from typing import Dict, List


@attr.s(auto_attribs=True)
class CacheItem:
    _resource: dict

    def __attrs_post_init__(self):
        self._lock: threading.Lock = threading.Lock()

    @property
    def resource(self) -> dict:
        return self._resource

    @property
    def name(self) -> str:
        return self._resource["metadata"]["name"]

    @property
    def spec(self) -> dict:
        return self._resource["spec"]

    @resource.setter
    def resource(self, new_values: dict):
        self._resource.update(new_values)

    def lock(self):
        self._lock.locked()

    def free(self):
        self._lock.release()


class Cache:
    def __init__(self):
        self._items: Dict[str, CacheItem] = dict()

    def list_item_names(self) -> List[str]:
        return list(self._items.keys())

    def insert(self, cache_item: CacheItem):
        self._items[cache_item.name] = cache_item

    def remove(self, item_name: str):
        del self._items[item_name]

    def get(self, item_name: str) -> CacheItem:
        return self._items.get(item_name)

