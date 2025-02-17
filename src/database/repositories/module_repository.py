from typing import List
from beanie import Document, PydanticObjectId
from api_requests.module_requests import CreateModuleRequest, PatchModuleRequest
from api_responses.module_responses import ModuleResponse
from database.models.module_model import Module
from database.models.project_model import Project
from database.repositories.base_repository import BaseRepository
from exceptions.module_exceptions import ModuleNotFoundException, UpdateModuleException
from exceptions.project_exceptions import ProjectNotFoundException

class ModuleRepository(BaseRepository):

    def __init__(self, module_model: Module):
        self.module_model = module_model

    async def get_by_id(
            self, 
            user_id: PydanticObjectId, 
            module_id: PydanticObjectId) -> ModuleResponse:
        
        module = await self.module_model.find_one(
            self.module_model.user_id == user_id,
            self.module_model.id == module_id
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
    
    async def create(self, user_id: PydanticObjectId, create_module_request: CreateModuleRequest):
        pass

    async def create(
            self, 
            user_id: PydanticObjectId, 
            project_id: PydanticObjectId, 
            create_module_request: CreateModuleRequest):

        project = await Project.find_one(
            Project.user_id == user_id,
            Project.id == project_id
        )

        if not project:
            raise ProjectNotFoundException("Couldn't find project or unauthorized.")
        
        module = self.module_model(
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
            patch_module_request: PatchModuleRequest):
        
        module = await self.module_model.find_one(
            self.module_model.user_id == user_id,
            self.module_model.id == module_id
        )

        if not module:
            raise ModuleNotFoundException("Couldn't find module or unauthorized.")
        
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
            raise UpdateModuleException("Error: Module update data in bad format.")
        
    async def delete(
            self, 
            user_id: PydanticObjectId, 
            module_id: PydanticObjectId):
        pass

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
            raise ProjectNotFoundException("Project not found or unauthorized.")
        
        module = await self.module_model.find_one(
            self.module_model.user_id == user_id,
            self.module_model.id == module_id
        )

        if not module or module_id not in project.modules:
            raise ModuleNotFoundException("Module not found or unauthorized.")
        
        await module.delete()
        project.modules.remove(module_id)
        await project.save()

    async def list(
        self,
        user_id: PydanticObjectId,
        project_id: PydanticObjectId
    ) -> List[ModuleResponse]:
        
        project = await Project.find_one(
            Project.user_id == user_id,
            Project.id == project_id
        )

        if not project:
            raise ProjectNotFoundException("Project not found or unauthorized")
        
        modules = await self.module_model.find(
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

        


        


