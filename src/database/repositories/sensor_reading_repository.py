from typing import List
from beanie import PydanticObjectId
from api_requests.sensor_reading_requests import CreateReadingRequest
from api_responses.sensor_reading_responses import SensorReadingResponse
from database.models.device_model import Device
from database.models.sensor_reading_model import SensorReading
from database.repositories.base_repository import BaseRepository
from exceptions.device_exceptions import DeviceNotFoundException

class SensorReadingRepository(BaseRepository):

    def __init__(self, sensor_reading_model: SensorReading):
        self.sensor_reading_model = sensor_reading_model

    async def create(self, user_id, obj_data):
        pass

    async def create(
            self, 
            user_id: PydanticObjectId, 
            device_id: PydanticObjectId,
            create_reading_request: CreateReadingRequest
    ) -> SensorReadingResponse:
        
        device = await Device.find_one(
            Device.user_id == user_id,
            Device.id == device_id
        )

        if not device:
            raise DeviceNotFoundException("Device not found or unauthorized.")
        
        sensor_reading = self.sensor_reading_model(
            user_id=user_id,
            device_id=device_id,
            data_type=create_reading_request.data_type,
            value=create_reading_request.value
        )
        await sensor_reading.insert()

        return SensorReadingResponse(
            id=str(sensor_reading.id),
            data_type=sensor_reading.data_type,
            value=sensor_reading.value,
            created_at=sensor_reading.created_at
        )
    
    async def get_by_id(self, user_id, obj_id):
        pass

    async def update(self, user_id, obj_id, update_data):
        pass

    async def delete(self, user_id, obj_id):
        pass
    
    async def list(
            self,
            user_id: PydanticObjectId,
            device_id: PydanticObjectId,
            date_filter: dict = None
    ) -> List[SensorReadingResponse]:
        
        device = await Device.find_one(
            Device.user_id == user_id,
            Device.id == device_id
        )

        if not device:
            raise DeviceNotFoundException("Device not found or unauthorized.")
        
        if date_filter:

            if "date" in date_filter:
                readings = await self.sensor_reading_model.find(
                    self.sensor_reading_model.device_id == device_id,
                    self.sensor_reading_model.created_at.date() == date_filter["date"]
                )
            elif "start_date" in date_filter and "end_date" in date_filter:
                readings = await self.sensor_reading_model.find(
                    self.sensor_reading_model.device_id == device_id,
                    self.sensor_reading_model.created_at.date() >= date_filter["start_date"],
                    self.sensor_reading_model.created_at.date() <= date_filter["end_date"]
                )
        else:
            readings = await self.sensor_reading_model.find(
                self.sensor_reading_model.device_id == device_id
            )
        readings_response = [
            SensorReadingResponse(
                id=str(reading.id),
                data_type=reading.data_type,
                value=reading.value,
                created_at=reading.created_at
            )
            for reading in readings
        ]

        return readings_response
