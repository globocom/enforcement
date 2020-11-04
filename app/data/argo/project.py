from argocd_client.models import v1_object_meta
import attr

from argocd_client import (
    ProjectServiceApi,
    V1alpha1AppProject,
    V1ObjectMeta,
    V1alpha1AppProjectSpec,
    V1alpha1AppProjectStatus,
    V1alpha1ApplicationDestination
)

from app.domain.entities import Cluster
from app.domain.repositories import ProjectRepository


@attr.s(auto_attribs=True)
class ProjectService(ProjectRepository):
    _project_service: ProjectServiceApi
 
    def create_project(self,  cluster: Cluster) -> None:
        project = V1alpha1AppProject(
            metadata=V1ObjectMeta(
                name=cluster.name,
                generate_name=cluster.name
            ),
            spec=V1alpha1AppProjectSpec(
                destinations=[V1alpha1ApplicationDestination(
                    server=cluster.url,
                    namespace='default',
                    name=cluster.name
                )],
                source_repos=['*']
            ),
            status=V1alpha1AppProjectStatus()
        )
       
        self._project_service.create_mixin6(project)

    def remove_project(self,  project_name: str) -> None:
        self._project_service.delete_mixin6(name=project_name)