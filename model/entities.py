from pydantic import BaseModel
from typing import Dict, Any, List


class Cluster(BaseModel):
    name: str
    token: str
    url: str
    id: str


class Helm(BaseModel):
    parameters: Dict[str, str] = None


class RancherSource(BaseModel):
    filters: Dict[str, str] = None
    labels: Dict[str, str] = None
    ignore: List[str] = None


class EnforcementSource(BaseModel):
    rancher: RancherSource = None


class Enforcement(BaseModel):
    name: str
    repo: str
    path: str = None
    namespace: str = "default"
    helm: Helm = None


class ClusterGroup(BaseModel):
    enforcements: List[Enforcement]
    source: EnforcementSource


class ClusterGroupStatus(BaseModel):
    clusters: List[str]





