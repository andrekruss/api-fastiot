from beanie import PydanticObjectId
from bson import ObjectId
import bson
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from api_requests.project_requests import CreateProjectRequest, PatchProjectRequest
from api_responses.project_responses import ProjectResponse
from database.models.project_model import Project
from database.models.user_model import User
from utils.auth import get_current_user
from utils.helper_functions import validate_object_id

project_router = APIRouter(prefix="/projects", tags=["projects"])

@project_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ProjectResponse)
async def create_project(create_project_request: CreateProjectRequest, user: User = Depends(get_current_user)):

    new_project = Project(
        user_id=user.id,
        name=create_project_request.name,
        description=create_project_request.description
    )
    await new_project.insert()
    return ProjectResponse(
        id=str(new_project.id),
        name=new_project.name,
        description=new_project.description
    )

@project_router.get("/get/{project_id}", status_code=status.HTTP_200_OK, response_model=ProjectResponse)
async def get_project(project_id: str, user: User = Depends(get_current_user)):

    project_object_id = validate_object_id(project_id)

    project = await Project.find_one(
        Project.id == project_object_id,
        Project.user_id == user.id
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )
    
    modules = list(map(str, project.modules))
    
    return ProjectResponse(
        id=str(project.id),
        name=project.name,
        description=project.description,
        modules=modules
    )

@project_router.get("/list", status_code=status.HTTP_200_OK, response_model=List[ProjectResponse])
async def list_projects(user: User = Depends(get_current_user)):

    projects = await Project.find({"user_id": user.id}).to_list()

    return [
        ProjectResponse(
            id=str(project.id),
            name=project.name,
            description=project.description,
            modules=list(map(str, project.modules)),
        )
        for project in projects
    ]

@project_router.delete("/delete/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(project_id: str, user: User = Depends(get_current_user)):

    project_object_id = validate_object_id(project_id)

    project = await Project.find_one(
        Project.id == project_object_id,
        Project.user_id == user.id
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied."
        )
    
    await project.delete()

@project_router.patch("/patch/{project_id}", status_code=status.HTTP_200_OK)
async def patch(
    project_id: str, 
    patch_project_request: PatchProjectRequest,
    user: User = Depends(get_current_user)
):
    
    project_object_id = validate_object_id(project_id)

    project = await Project.find_one(
        Project.id == project_object_id,
        Project.user_id == user.id
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied."
        )
    
    update_data = {key: value for key, value in patch_project_request.model_dump(exclude_unset=True).items()}

    if update_data:
        await project.update({"$set": update_data})
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields provided for update."
        )
    
    return ProjectResponse(
        id=str(project.id),
        name=project.name,
        description=project.description,
        modules=project.modules
    )
