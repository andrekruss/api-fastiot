from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from api_requests.sensor_reading_requests import CreateReadingRequest
from api_responses.sensor_reading_responses import SensorReadingResponse
from database.models.sensor_reading_model import SensorReading
from database.models.user_model import User
from database.repositories.sensor_reading_repository import SensorReadingRepository
from exceptions.device_exceptions import DeviceNotFoundException
from utils.auth import get_current_user
from utils.helper_functions import validate_object_id

sensor_reading_repository = SensorReadingRepository(SensorReading)
sensor_reading_router = APIRouter(prefix="/sensor-readings", tags=["sensor-readings"])

@sensor_reading_router.post(path="/create/{device_id}", status_code=status.HTTP_201_CREATED, response_model=SensorReadingResponse)
async def create_sensor_reading(device_id: str, create_reading_request: CreateReadingRequest, user: User = Depends(get_current_user)):

    try:
        device_object_id = validate_object_id(device_id)
        sensor_reading = await sensor_reading_repository.create(
            user_id=user.id,
            device_id=device_object_id
        )
        return sensor_reading
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
    
@sensor_reading_repository.get(path="/list/{device_id}", status_code=status.HTTP_200_OK, response_model=SensorReadingResponse)
async def list(
    device_id: str, 
    date: Optional[date] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    user: User = Depends(get_current_user)
):

    try:

        device_object_id = validate_object_id(device_id)

        if date:
            readings = await sensor_reading_repository.list(
                user_id=user.id,
                device_id=device_object_id,
                date_filter={"date": date}
            )
        elif start_date and end_date:
            readings = await sensor_reading_repository.list(
                user_id=user.id,
                device_id=device_object_id,
                date_filter={"start_date": start_date, "end_date": end_date}
            )
        else:
            readings = await sensor_reading_repository.list(
                user_id=user.id,
                device_id=device_object_id
            )
        return readings
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