from dataclasses import dataclass, field
from typing import Dict, List, Callable

from helper import Config

from argocd_client import V1alpha1ApplicationSource, V1alpha1ApplicationSourceHelm, V1alpha1HelmParameter

from model.cluster import Cluster


@dataclass
class Enforcement:
    repo: str
    path: str
    cluster_name: str
    name: str
    _labels: Dict[str, str] = field(default_factory=dict)

    def add_label(self, name: str, value: str) -> None:
        self._labels[name] = value

    def render(self) -> V1alpha1ApplicationSource:
        source = V1alpha1ApplicationSource(path=self.path, repo_url=self.repo)
        return source

    @property
    def labels(self) -> Dict[str, str]:
        return self._labels


@dataclass
class EnforcementHelm(Enforcement):
    params: List[Dict[str, str]] = field(default_factory=list)

    def render(self) -> V1alpha1ApplicationSource:
        source = super().render()

        source.helm = V1alpha1ApplicationSourceHelm(parameters=[
            V1alpha1HelmParameter(
                name=param["name"],
                value=param["value"]
            )
            for param in self.params
        ])
        return source

    def add_parameter(self, name: str, value: str) -> None:
        self.params.append({"name": name, "value": value})


def make_default_enforcement(cluster_name: str, config: Config) -> Callable[[Cluster], EnforcementHelm]:
    default_enforcement = EnforcementHelm(
        repo=config.enforcement_core_repo,
        path=config.enforcement_core_path,
        cluster_name='in-cluster',
        name=f"{cluster_name}-{config.enforcement_name}",
    )

    default_enforcement.add_label("cluster", cluster_name)

    default_enforcement.add_parameter('spec.destination.name', cluster_name)
    return lambda _self: default_enforcement
