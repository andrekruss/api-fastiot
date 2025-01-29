from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, Response, status, HTTPException

from api_requests.module_requests import CreateModuleRequest, PatchModuleRequest
from api_responses.module_responses import ModuleResponse
from database.models.module_model import Module
from database.models.project_model import Project
from database.models.user_model import User
from utils.auth import get_current_user

module_router = APIRouter(prefix="/modules", tags=["modules"])

@module_router.post("/create/{project_id}", status_code=status.HTTP_201_CREATED, response_model=ModuleResponse)
async def create_module(project_id: str, create_module_request: CreateModuleRequest, user: User = Depends(get_current_user)):

    project_object_id = ObjectId(project_id)

    project = await Project.find_one(
        Project.id == project_object_id,
        Project.user_id == user.id
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )
    
    new_module = Module(
        project_id=project_object_id,
        name=create_module_request.name,
        description=create_module_request.description
    )

    await new_module.insert()

    project.modules.append(ObjectId(new_module.id))
    await project.save()

    return ModuleResponse(
        id=str(new_module.id),
        user_id=str(user.id),
        project_id=str(project_object_id),
        name=new_module.name,
        description=new_module.description
    )

@module_router.get("/get/{project_id}/{module_id}", status_code=status.HTTP_200_OK, response_model=ModuleResponse)
async def get_module(project_id: str, module_id: str, user: User = Depends(get_current_user)):

    user_object_id = ObjectId(user.id)
    project_object_id = ObjectId(project_id)
    module_object_id = ObjectId(module_id)

    project = await Project.find_one(
        Project.user_id == user_object_id,
        Project.id == project_object_id
    )

    if not project or module_object_id not in project.modules:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or module does not belong to project."
        )
    
    module = await Module.find_one(
        Module.id == module_object_id
    )

    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module was not found."
        )

    return ModuleResponse(
        id=module_id,
        user_id=str(user_object_id),
        project_id=project_id,
        name=module.name,
        description=module.description,
        devices=list(map(str, module.devices))
    )

@module_router.get("/list/{project_id}", status_code=status.HTTP_200_OK, response_model=List[ModuleResponse])
async def list_modules(project_id: str, user: User = Depends(get_current_user)):
    
    user_object_id = ObjectId(user.id)
    project_object_id = ObjectId(project_id)
    
    project = await Project.find_one(
        Project.user_id == user_object_id,
        Project.id == project_object_id
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find project"
        )
    
    if not project.modules:
        return []

    modules = await Module.find(
        {"_id": {"$in": project.modules}}
    ).to_list(length=len(project.modules))

    modules_response = [
        ModuleResponse(
            id=str(module.id),
            user_id=str(user.id),
            project_id=project_id,
            name=module.name,
            description=module.description,
            devices=list(map(str, module.devices)) if module.devices else []
        )
        for module in modules
    ]

    return modules_response

@module_router.delete("/delete/{project_id}/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_module(module_id: str, project_id: str, user: User = Depends(get_current_user)):

    user_object_id = ObjectId(user.id)
    project_object_id = ObjectId(project_id)
    module_object_id = ObjectId(module_id)

    project = await Project.find_one(
        Project.user_id == user_object_id,
        Project.id == project_object_id
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find project."
        )
    
    if module_object_id not in project.modules:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find module."
        )
    
    module = await Module.find_one(Module.id == module_object_id)
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found in database."
        )
    await module.delete()

    project.modules.remove(module_object_id)
    await project.save()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@module_router.patch("/patch/{project_id}/{module_id}", status_code=status.HTTP_200_OK)
async def patch_module(project_id: str, module_id: str, patch_module_request: PatchModuleRequest, user: User = Depends(get_current_user)):

    user_object_id = ObjectId(user.id)
    project_object_id = ObjectId(project_id)
    module_object_id = ObjectId(module_id)

    project = await Project.find_one(
        Project.user_id == user_object_id,
        Project.id == project_object_id
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find project."
        )
    
    if module_object_id not in project.modules:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find module."
        )
    
    module = await Module.find_one(Module.id == module_object_id)
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found in database."
        )

    update_data = {key: value for key, value in patch_module_request.model_dump(exclude_unset=True).items()}

    if update_data:
        await module.update({"$set": update_data})
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields provided for update."
        )
    
    return ModuleResponse(
        id=module_id,
        user_id=str(user.id),
        project_id=project_id,
        name=module.name,
        description=module.description,
        devices=list(map(str, module.devices))
    )

