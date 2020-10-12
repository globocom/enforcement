from dataclasses import dataclass


@dataclass
class Cluster:
    name: str
    token: str
    url: str
    id: str

