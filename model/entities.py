from dataclasses import dataclass
from pydantic import BaseModel
from typing import Dict, Any, List


@dataclass
class Cluster:
    name: str
    token: str
    url: str
    id: str


class Helm(BaseModel):
    parameters: Dict[str, Any] = None


class RancherSource(BaseModel):
    filters: Dict[str, str] = None
    labels: Dict[str, str] = None
    ignore: List[str] = None


class EnforcementSource(BaseModel):
    rancher: RancherSource = None


class Enforcement(BaseModel):
    name: str
    repo: str
    helm: Helm = None


class ClusterGroup(BaseModel):
    enforcements: List[Enforcement]
    source: EnforcementSource




