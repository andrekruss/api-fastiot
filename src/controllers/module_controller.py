from typing import List
from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import APIRouter, Body, Depends, Response, status, HTTPException

from api_requests.module_requests import CreateModuleRequest, PatchModuleRequest
from api_responses.module_responses import ModuleResponse
from database.models.module_model import Module
from database.models.project_model import Project
from database.models.user_model import User
from database.repositories.module_repository import ModuleRepository
from exceptions.module_exceptions import ModuleNotFoundException, UpdateModuleException
from exceptions.project_exceptions import ProjectNotFoundException
from utils.auth import get_current_user
from utils.helper_functions import validate_object_id

module_repository = ModuleRepository(Module)
module_router = APIRouter(prefix="/modules", tags=["modules"])

@module_router.post("/create/{project_id}", status_code=status.HTTP_201_CREATED, response_model=ModuleResponse)
async def create_module(project_id: str, create_module_request: CreateModuleRequest = Body(...), user: User = Depends(get_current_user)):
    try:
        project_object_id = validate_object_id(project_id)
        module = await module_repository.create(user.id, project_object_id, create_module_request)
        return module
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

@module_router.get("/get/{module_id}", status_code=status.HTTP_200_OK, response_model=ModuleResponse)
async def get_module(module_id: str, user: User = Depends(get_current_user)):

    try:
        module_object_id = validate_object_id(module_id)
        module = await module_repository.get_by_id(
            user.id,
            module_object_id
        )
        return module
    except ModuleNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )
    

@module_router.get("/list/{project_id}", status_code=status.HTTP_200_OK, response_model=List[ModuleResponse])
async def list_modules(project_id: str, user: User = Depends(get_current_user)):
    
    try:
        project_object_id = validate_object_id(project_id)
        modules = await module_repository.list(user.id, project_object_id)
        return modules
    except ProjectNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )
    

@module_router.delete("/delete/{project_id}/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_module(project_id: str, module_id: str, user: User = Depends(get_current_user)):

    try:
        module_object_id = validate_object_id(module_id)
        project_object_id = validate_object_id(project_id)
        await module_repository.delete(
            user.id,
            project_object_id,
            module_object_id
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ModuleNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )
    except ProjectNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )
    

@module_router.patch("/patch/{module_id}", status_code=status.HTTP_200_OK, response_model=ModuleResponse)
async def patch_module(
    module_id: str, 
    patch_module_request: PatchModuleRequest = Body(...), 
    user: User = Depends(get_current_user)):

    try:
        module_object_id = validate_object_id(module_id)    
        updated_module = await module_repository.update(
            user.id,
            module_object_id,
            patch_module_request
        )
        return updated_module
    except ModuleNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )
    except UpdateModuleException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )


