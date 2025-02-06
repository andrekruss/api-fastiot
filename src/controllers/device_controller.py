from typing import List
from beanie import PydanticObjectId
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
from utils.helper_functions import validate_object_id

device_router = APIRouter(prefix="/devices", tags=["devices"])

@device_router.post("/create/{module_id}", status_code=status.HTTP_201_CREATED, response_model=DeviceResponse)
async def create_device(create_device_request: CreateDeviceRequest, module_id: str, user: User = Depends(get_current_user)):

    module_object_id = validate_object_id(module_id)
    
    module = await Module.find_one(
        Module.user_id == user.id,
        Module.id == module_object_id
    )

    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found."
        )
    
    new_device = Device(
        module_id=module_object_id,
        user_id=user.id,
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

@device_router.get("/get/{device_id}", status_code=status.HTTP_200_OK, response_model=DeviceResponse)
async def get_device(device_id: str, user: User = Depends(get_current_user)):

    device_object_id = validate_object_id(device_id)

    device = await Device.find_one(
        Device.user_id == user.id,
        Device.id == device_object_id
    )

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found."
        )
    
    return DeviceResponse(
        id=str(device.id),
        name=device.name,
        description=device.description,
        device_type=device.device_type
    )

@device_router.get("/list/{module_id}", status_code=status.HTTP_200_OK, response_model=List[DeviceResponse])
async def list_modules(module_id: str, user: User = Depends(get_current_user)):

    try:
        module_object_id = PydanticObjectId(module_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid module ID format")

    module = await Module.find_one(
        Module.id == module_object_id,
        Module.user_id == user.id
    )

    if not module:
        raise HTTPException(status_code=403, detail="Module not found or unauthorized")

    devices = await Device.find(
        Device.user_id == user.id,
        Device.module_id == module_object_id
    ).to_list()

    devices_response = [
        DeviceResponse(
            id=str(device.id),
            name=device.name,
            description=device.description,
            device_type=device.device_type
        )
        for device in devices
    ]

    return devices_response