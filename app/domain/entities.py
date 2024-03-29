from typing import Dict, List

from pydantic import BaseModel


class Cluster(BaseModel):
    name: str
    url: str
    token: str
    id: str
    additional_data: dict = dict()


class Helm(BaseModel):
    parameters: Dict[str, str] = None


class RancherSource(BaseModel):
    filters: Dict[str, str] = None
    labels: Dict[str, str] = None
    ignore: List[str] = None


class EnforcementSource(BaseModel):
    rancher: RancherSource = None
    secretName: str = None


class Enforcement(BaseModel):
    name: str
    repo: str
    path: str = None
    namespace: str = "default"
    helm: Helm = None
    labels: dict = None


class TriggerConfig(BaseModel):
    endpoint: str
    timeout: int = 5


class TriggersConfig(BaseModel):
    beforeInstall: TriggerConfig = None
    afterInstall: TriggerConfig = None


class ClusterRule(BaseModel):
    enforcements: List[Enforcement]
    source: EnforcementSource
    triggers: TriggersConfig = None


class ClusterRuleStatus(BaseModel):
    clusters: List[dict] = []
    install_errors: List[str] = []


class Secret(BaseModel):
    token: str
    url: str


