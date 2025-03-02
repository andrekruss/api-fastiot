from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi import status

from api_requests.device_requests import CreateDeviceRequest
from api_responses.device_responses import DeviceResponse
from database.models.device_model import Device
from database.models.user_model import User
from database.repositories.device_repository import DeviceRepository
from exceptions.device_exceptions import DeviceNotFoundException
from exceptions.module_exceptions import ModuleNotFoundException
from utils.auth import get_current_user
from utils.helper_functions import validate_object_id

device_repository = DeviceRepository(Device)
device_router = APIRouter(prefix="/devices", tags=["devices"])

@device_router.post("/create/{module_id}", status_code=status.HTTP_201_CREATED, response_model=DeviceResponse)
async def create_device(module_id: str, create_device_request: CreateDeviceRequest = Body(...), user: User = Depends(get_current_user)):

    try:
        module_object_id = validate_object_id(module_id)
        device = await device_repository.create(user.id, module_object_id, create_device_request)
        return device
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


@device_router.get("/get/{module_id}/{device_id}", status_code=status.HTTP_200_OK, response_model=DeviceResponse)
async def get_device(module_id: str, device_id: str, user: User = Depends(get_current_user)):

    try:
        module_object_id = validate_object_id(module_id)
        device_object_id = validate_object_id(device_id)
        device = await device_repository.get_by_id(user.id, module_object_id, device_object_id)
        return device
    except ModuleNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )
    except DeviceNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )

@device_router.get("/list/{module_id}", status_code=status.HTTP_200_OK, response_model=List[DeviceResponse])
async def list_devices(module_id: str, user: User = Depends(get_current_user)):

    try:
        module_object_id = validate_object_id(module_id)
        devices = await device_repository.list(user.id, module_object_id)
        return devices
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