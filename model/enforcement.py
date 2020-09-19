from dataclasses import dataclass, field
from typing import List

from argocd_client import V1alpha1ApplicationSource, V1alpha1ApplicationSourceHelm, V1alpha1HelmParameter


@dataclass
class Enforcement:
    repo: str
    path: str
    name: str

    def render(self) -> V1alpha1ApplicationSource:
        source = V1alpha1ApplicationSource(path=self.path, repo_url=self.repo)
        return source


@dataclass
class EnforcementHelm(Enforcement):
    params: List[dict] = field(default=[])

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
        self.params.append({name: value})


