from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status

from api_requests.device_requests import CreateDeviceRequest
from api_responses.device_responses import DeviceResponse
from database.models.device_model import Device
from database.models.module_model import Module
from database.models.project_model import Project
from database.models.user_model import User
from utils.auth import get_current_user

device_router = APIRouter(prefix="/devices", tags=["devices"])

@device_router.post("/create/{project_id}/{module_id}", status_code=status.HTTP_201_CREATED)
async def create_device(create_device_request: CreateDeviceRequest, project_id: str, module_id: str, user: User = Depends(get_current_user)):

    project_object_id = ObjectId(project_id)
    module_object_id = ObjectId(module_id)

    project = await Project.find_one(
        Project.id == project_object_id,
        Project.user_id == user.id
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )
    
    module = await Module.find_one(
        Module.project_id == project_object_id,
        Module.id == module_object_id
    )

    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )
    
    new_device = Device(
        module_id=module_object_id,
        name=create_device_request.name,
        description=create_device_request.description,
        device_type=create_device_request.device_type
    )

    await new_device.insert()
    module.devices.append(new_device.id)
    await module.save()

    return DeviceResponse(
        id=str(new_device.id),
        name=new_device.name,
        description=new_device.description,
        device_type=new_device.device_type
    )
