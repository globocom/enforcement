from enum import Enum
import attr
from typing import ClassVar


class Type(Enum):
    CREATE = 1
    UPDATE = 2
    REMOVE = 3
    TIME = 4


@attr.s(auto_attribs=True)
class Event:
    cluster_rule: dict
    type: Type


class DetectorRule:

    def add_next_rule(self, next_rule):
        self.next_rule = next_rule

    def detect(self, event_map: dict):
        raise Exception('Not implemented')

    @classmethod
    def new_event(cls, event_type: Type, event_map: dict) -> Event:
        return Event(type=event_type, cluster_rule=event_map["object"])


@attr.s(auto_attribs=True)
class RemoveDetectorRule(DetectorRule):
    def detect(self, event_map: dict) -> Event:
        if event_map["type"] == "DELETED":
            return self.new_event(Type.REMOVE, event_map)

        return self.next_rule.detect(event_map)


@attr.s(auto_attribs=True)
class CreateDetectorRule(DetectorRule):
    CREATE_ANNOTATION: ClassVar[str] = "enforcement.created"

    def detect(self, event_map: dict) -> Event:
        annotations = event_map["object"]["metadata"]["annotations"]

        if event_map["type"] == "ADDED":
            if self.CREATE_ANNOTATION not in annotations:
                return self.new_event(Type.CREATE, event_map)

        return self.next_rule.detect(event_map)


@attr.s(auto_attribs=True)
class OnlineUpdateDetectorRule(DetectorRule):

    def detect(self, event_map: dict) -> Event:
        if event_map["type"] == "MODIFIED":
            return self.new_event(Type.UPDATE, event_map)

        return self.next_rule.detect(event_map)


class NotFoundDetectRule(DetectorRule):
    def detect(self, event_map: dict):
        return None


class EventDetector:

    def __init__(self):
        remove_rule = RemoveDetectorRule()
        create_rule = CreateDetectorRule()
        online_update_rule = OnlineUpdateDetectorRule()

        remove_rule.add_next_rule(online_update_rule)
        online_update_rule.add_next_rule(create_rule)
        create_rule.add_next_rule(NotFoundDetectRule())

        self._detectors_chain = remove_rule

    def detect(self, event_map: dict) -> Event:
        event = self._detectors_chain.detect(event_map)
        if event:
            return event
        else:
            raise Exception("Event Not Found")

