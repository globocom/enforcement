from typing import List, NamedTuple
from app.domain.entities import Cluster, Enforcement

RulesResponse = NamedTuple("RulesResponse", [
    ('clusters', List[Cluster]),
    ('install_errors', List[Enforcement])
])

UpdateRulesResponse = NamedTuple("UpdateRulesResponse", [
    ('install_errors', List[Enforcement]),
    ('update_errors', List[Enforcement])
])

SyncRulesResponse = NamedTuple("SyncRulesResponse", [
    ('clusters', List[Cluster]),
])
