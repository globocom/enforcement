from dataclasses import dataclass, field
from typing import List, Callable

from helper import Config

from argocd_client import V1alpha1ApplicationSource, V1alpha1ApplicationSourceHelm, V1alpha1HelmParameter


@dataclass
class Enforcement:
    repo: str
    path: str
    cluster_name: str
    name: str

    def render(self) -> V1alpha1ApplicationSource:
        source = V1alpha1ApplicationSource(path=self.path, repo_url=self.repo)
        return source


@dataclass
class EnforcementHelm(Enforcement):
    params: List[dict] = field(default_factory=list)

    def render(self):
        source = super().render()

        source.helm = V1alpha1ApplicationSourceHelm(parameters=[
            V1alpha1HelmParameter(
                name=param["name"],
                value=param["value"]
            )
            for param in self.params
        ])
        return source

    def add_parameter(self, name: str, value: str):
        self.params.append({"name": name, "value": value})


def make_default_enforcement(cluster_name: str, config: Config) -> Callable[[], EnforcementHelm]:
    default_enforcement = EnforcementHelm(
        repo=config.enforcement_core_repo,
        path=config.enforcement_core_path,
        cluster_name='in-cluster',
        name=f"{cluster_name}-{config.enforcement_name}",
    )

    default_enforcement.add_parameter('spec.destination.name', cluster_name)
    return lambda: default_enforcement
