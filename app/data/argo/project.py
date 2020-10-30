from typing import Dict, List
import attr

from argocd_client import (
    ProjectServiceApi,
    V1alpha1AppProject,
    V1ObjectMeta,
    V1alpha1AppProjectSpec,
    V1alpha1AppProjectStatus
)

from app.domain.entities import Project
from app.domain.repositories import ProjectRepository


@attr.s(auto_attribs=True)
class ProjectService(ProjectRepository):
    _project_service: ProjectServiceApi
 
    def create_project(self,  project: Project) -> None:
        argo_project = V1alpha1AppProject(
            metadata=V1ObjectMeta(
                name=project.name
            )
        )
        _project_service.create_mixin6(body=argo_project)

    def remove_project(self,  project: Project) -> None:
        _project_service.delete_mixin6(name=project.name)