from ast import Module
from typing import List
from beanie import PydanticObjectId
from api_requests.project_requests import CreateProjectRequest, PatchProjectRequest
from api_responses.project_responses import ProjectResponse
from database.models.device_model import Device
from database.models.project_model import Project
from database.models.sensor_reading_model import SensorReading
from database.repositories.base_repository import BaseRepository
from exceptions.project_exceptions import ProjectNotFoundException, UpdateProjectException

class ProjectRepository(
    BaseRepository[
        Project,
        ProjectResponse,
        CreateProjectRequest,
        PatchProjectRequest
    ]):
    "Repository for project CRUD operations."

    def __init__(self):
        super().__init__(Project)

    async def get(self, user_id: PydanticObjectId, project_id: PydanticObjectId) -> ProjectResponse:
        
        project = await self.model.find_one(
            self.model.user_id == user_id,
            self.model.id == project_id
        )

        if not project:
            raise ProjectNotFoundException()
        
        modules = list(map(str, project.modules))

        return ProjectResponse(
            id=str(project.id),
            name=project.name,
            description=project.description,
            modules=modules
        )
    
    async def get_all(self, user_id: PydanticObjectId) -> List[ProjectResponse]:

        projects = await self.model.find(
            self.model.user_id == user_id
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
    
    async def create(self, user_id: PydanticObjectId, create_project_request: CreateProjectRequest) -> ProjectResponse:

        project = self.model(
            user_id=user_id,
            name=create_project_request.name,
            description=create_project_request.description,
            modules=[]
        )

        await project.insert()
        
        modules = list(map(str, project.modules))

        return ProjectResponse(
            id=str(project.id),
            name=project.name,
            description=project.description,
            modules=modules
        )
    
    async def update(
            self, 
            user_id: PydanticObjectId, 
            project_id: PydanticObjectId, 
            patch_project_request: PatchProjectRequest
        ) -> ProjectResponse:
        
        project = await self.project_model.find_one(
            self.model.user_id == user_id,
            self.model.id == project_id
        )

        if not project:
            raise ProjectNotFoundException()

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

        project = await self.model.find_one(
            self.model.user_id == user_id,
            self.model.id == project_id
        )

        if not project:
            raise ProjectNotFoundException("Project not found.")

        if not project.modules:
            return

        module_ids = project.modules

        device_ids = await Device.find(Device.module_id.in_(module_ids)).distinct(Device.id)

        await SensorReading.delete_many(SensorReading.device_id.in_(device_ids))

        await Device.delete_many(Device.module_id.in_(module_ids))

        await Module.delete_many(Module.id.in_(module_ids))

        await project.delete()

    async def exists(self, project_id: PydanticObjectId) -> bool:

        project = await self.model.find_one(
            self.model.id == project_id
        )

        if project:
            return True
        
        return False








    
