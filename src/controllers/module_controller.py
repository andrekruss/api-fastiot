from bson import ObjectId
from fastapi import APIRouter, Depends, status, HTTPException

from api_requests.module_requests import CreateModuleRequest
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




