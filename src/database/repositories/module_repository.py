from typing import List
from beanie import Document, PydanticObjectId
from api_requests.module_requests import CreateModuleRequest, PatchModuleRequest
from api_responses.module_responses import ModuleResponse
from database.models.device_model import Device
from database.models.module_model import Module
from database.models.project_model import Project
from database.models.sensor_reading_model import SensorReading
from database.repositories.base_repository import BaseRepository
from database.repositories.device_repository import DeviceRepository
from database.repositories.project_repository import ProjectRepository
from exceptions.module_exceptions import ModuleNotFoundException, BadUpdateDataException
from exceptions.project_exceptions import ProjectNotFoundException

class ModuleRepository(
    BaseRepository[
        Module,
        ModuleResponse,
        CreateModuleRequest,
        PatchModuleRequest
    ]):

    def __init__(self):
        super().__init__(Module)

    async def get(
            self, 
            user_id: PydanticObjectId, 
            module_id: PydanticObjectId) -> ModuleResponse:
        
        module = await self.model.find_one(
            self.model.user_id == user_id,
            self.model.id == module_id
        )

        if not module:
            raise ModuleNotFoundException("Couldn't find module or unauthorized.")
        
        devices = list(map(str, module.devices))

        return ModuleResponse(
            id=str(module.id),
            name=module.name,
            description=module.description,
            devices=devices
        )
    
    async def get_all(
        self,
        user_id: PydanticObjectId,
        project_id: PydanticObjectId
    ) -> List[ModuleResponse]:
        
        project_repository = ProjectRepository()
        
        project = await project_repository.get(
            user_id,
            project_id
        )

        if not project:
            raise ProjectNotFoundException()
        
        modules = await self.model.find(
            {"_id": {"$in": project.modules}}
        ).to_list(length=len(project.modules))

        modules_response = [
            ModuleResponse(
                id=str(module.id),
                name=module.name,
                description=module.description,
                devices=list(map(str, module.devices)) if module.devices else []
            )
            for module in modules
        ]

        return modules_response

    async def create(
            self, 
            user_id: PydanticObjectId, 
            project_id: PydanticObjectId, 
            create_module_request: CreateModuleRequest):

        project_repository = ProjectRepository()

        project = await project_repository.get(
            user_id,
            project_id
        )

        if not project:
            raise ProjectNotFoundException()
        
        module = self.model(
            user_id=user_id,
            project_id=project_id,
            name=create_module_request.name,
            description=create_module_request.description
        )

        await module.insert()

        project.modules.append(module.id)
        await project.save()
        
        return ModuleResponse(
            id=str(module.id),
            name=module.name,
            description=module.description
        )
    
    async def update(
            self, 
            user_id: PydanticObjectId, 
            module_id: PydanticObjectId, 
            patch_module_request: PatchModuleRequest) -> ModuleResponse:
        
        module = await self.model.find_one(
            self.model.user_id == user_id,
            self.model.id == module_id
        )

        if not module:
            raise ModuleNotFoundException()
        
        update_data = {key: value for key, value in patch_module_request.model_dump(exclude_unset=True).items()}

        if update_data:
            await module.update({"$set": update_data})
            return ModuleResponse(
                id=module_id,
                name=module.name,
                description=module.description,
                devices=list(map(str, module.devices))
            )
        else:
            raise BadUpdateDataException()

    async def delete(
            self,
            user_id: PydanticObjectId,
            project_id: PydanticObjectId,
            module_id: PydanticObjectId
    ):
    
        project = await Project.find_one(
            Project.user_id == user_id,
            Project.id == project_id
        )

        if not project:
            raise ProjectNotFoundException()
        
        if module_id not in project.modules:
            raise ModuleNotFoundException("Module does not belong to informed project.")
        
        module = await self.model.find_one(
            self.model.user_id == user_id,
            self.model.id == module_id
        )

        if not module:
            raise ModuleNotFoundException()
        
        device_ids = module.devices

        await SensorReading.delete_many(SensorReading.device_id.in_(device_ids))
        await Device.delete_many(Device.module_id == module_id)
        await module.delete()

    async def exists(self, module_id: PydanticObjectId):
        
        module = await self.model.find_one(
            self.model.id == module_id
        )

        if module:
            return True
        
        return False

    
    

        


        


