from beanie import PydanticObjectId
from bson import ObjectId
import bson
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from api_requests.project_requests import CreateProjectRequest, PatchProjectRequest
from api_responses.project_responses import ProjectResponse
from database.models.project_model import Project
from database.models.user_model import User
from database.repositories.project_repository import ProjectRepository
from exceptions.project_exceptions import ProjectNotFoundException, UpdateProjectException
from utils.auth import get_current_user
from utils.helper_functions import validate_object_id

project_repository = ProjectRepository(Project)
project_router = APIRouter(prefix="/projects", tags=["projects"])

@project_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ProjectResponse)
async def create_project(create_project_request: CreateProjectRequest, user: User = Depends(get_current_user)):

    new_project = await project_repository.create(user.id, create_project_request)
    return new_project

@project_router.get("/get/{project_id}", status_code=status.HTTP_200_OK, response_model=ProjectResponse)
async def get_project(project_id: str, user: User = Depends(get_current_user)):

    try:
        project_object_id = validate_object_id(project_id)
        project = await project_repository.get_by_id(user.id, project_object_id)
        return project
    except ProjectNotFoundException as err:
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(err)
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )


@project_router.get("/list", status_code=status.HTTP_200_OK, response_model=List[ProjectResponse])
async def list_projects(user: User = Depends(get_current_user)):
    return await project_repository.list(user.id)

@project_router.delete("/delete/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(project_id: str, user: User = Depends(get_current_user)):

    try:
        project_object_id = validate_object_id(project_id)
        await project_repository.delete(user.id, project_object_id)
    except ProjectNotFoundException as err:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(err)
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )

@project_router.patch("/patch/{project_id}", status_code=status.HTTP_200_OK)
async def patch(
    project_id: str, 
    patch_project_request: PatchProjectRequest,
    user: User = Depends(get_current_user)
):
    
    try:
        project_object_id = validate_object_id(project_id)
        project = await project_repository.update(
            user.id,
            project_object_id,
            patch_project_request
        )
        return project
    except ProjectNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )
    except UpdateProjectException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )
    
