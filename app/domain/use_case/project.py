import attr
from app.domain.repositories import ProjectRepository

@attr.s(auto_attribs=True)
class ProjectUseCase:
     _project_repository: ProjectRepository

     def _create(self):
          pass

     def _remove(self):
          pass