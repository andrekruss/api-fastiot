from typing import List
from beanie import PydanticObjectId
from api_requests.project_requests import CreateProjectRequest, PatchProjectRequest
from api_responses.project_responses import ProjectResponse
from database.models.project_model import Project
from database.repositories.base_repository import BaseRepository
from exceptions.project_exceptions import ProjectNotFoundException, UpdateProjectException

class ProjectRepository(BaseRepository):
    "Repository for project CRUD operations."

    def __init__(self, project_model: Project):
        self.project_model = project_model

    async def get_by_id(self, user_id: PydanticObjectId, project_id: PydanticObjectId) -> ProjectResponse:
        
        project = await self.project_model.find_one(
            self.project_model.user_id == user_id,
            self.project_model.id == project_id
        )

        if not project:
            raise ProjectNotFoundException("Project not found.")
        
        modules = list(map(str, project.modules))

        return ProjectResponse(
            id=str(project.id),
            name=project.name,
            description=project.description,
            modules=modules
        )
    
    async def create(self, user_id: PydanticObjectId, create_project_request: CreateProjectRequest) -> ProjectResponse:

        project = self.project_model(
            user_id=user_id,
            name=create_project_request.name,
            description=create_project_request.description
        )

        await project.insert()
        
        modules = list(map(str, project.modules))

        return ProjectResponse(
            id=str(project.id),
            name=project.name,
            description=project.description,
            modules=modules
        )
    
    async def list(self, user_id: PydanticObjectId) -> List[ProjectResponse]:

        projects = await self.project_model.find(
            self.project_model.user_id == user_id
        ).to_list()

        return [
            ProjectResponse(
                id=str(project.id),
                name=project.name,
                description=project.description,
                modules=list(map(str, project.modules)),
            )
            for project in projects
        ]
    
    async def update(
            self, 
            user_id: PydanticObjectId, 
            project_id: PydanticObjectId, 
            patch_project_request: PatchProjectRequest
        ) -> ProjectResponse:
        
        project = await self.project_model.find_one(
            self.project_model.user_id == user_id,
            self.project_model.id == project_id
        )

        if not project:
            raise ProjectNotFoundException("Project not found.")

        update_data = {key: value for key, value in patch_project_request.model_dump(exclude_unset=True).items()}

        if update_data:
            await project.update({"$set": update_data})
            return ProjectResponse(
                id=str(project.id),
                name=project.name,
                description=project.description,
                modules=list(map(str, project.modules))
            )
        else:
            raise UpdateProjectException("Error while parsing update data.")
    
    async def delete(self, user_id: PydanticObjectId, project_id: PydanticObjectId):
        
        project = await self.project_model.find_one(
            self.project_model.user_id == user_id,
            self.project_model.id == project_id
        )

        if not project:
            raise ProjectNotFoundException("Project not found.")
        
        await project.delete()




    
