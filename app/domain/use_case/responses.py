from typing import List, NamedTuple
from app.domain.entities import Cluster, Enforcement

RulesResponse = NamedTuple("RulesResponse", [
    ('clusters', List[Cluster]),
    ('install_errors', List[Enforcement])
])
