from typing import List
from beanie import PydanticObjectId

from api_requests.device_requests import CreateDeviceRequest
from api_responses.device_responses import DeviceResponse
from database.models.device_model import Device
from database.models.module_model import Module
from database.models.sensor_reading_model import SensorReading
from database.repositories.base_repository import BaseRepository
from exceptions.device_exceptions import DeviceNotFoundException
from exceptions.module_exceptions import ModuleNotFoundException

class DeviceRepository(
    BaseRepository[
        Device,
        DeviceResponse,
        CreateDeviceRequest,
        None
    ]):

    def __init__(self):
        super().__init__(Device)

    async def create(
            self, 
            user_id: PydanticObjectId,
            module_id: PydanticObjectId,
            create_device_request: CreateDeviceRequest
    ) -> DeviceResponse:
        
        module = await Module.find_one(
            Module.user_id == user_id,
            Module.id == module_id
        )

        if not module:
            raise ModuleNotFoundException("Module not found or unauthorized")
        
        device = self.model(
            module_id=module_id,
            user_id=user_id,
            name=create_device_request.name,
            description=create_device_request.description,
            device_type=create_device_request.device_type,
            data_types=create_device_request.data_types
        )
        
        await device.insert()
        module.devices.append(device.id)
        await module.save()

        return DeviceResponse(
            id=str(device.id),
            name=device.name,
            description=device.description,
            device_type=device.device_type,
            data_types=device.data_types
        )

    async def get(
            self,
            user_id: PydanticObjectId,
            module_id: PydanticObjectId,
            device_id: PydanticObjectId
    ) -> DeviceResponse:
        
        module = await Module.find_one(
            Module.user_id == user_id,
            Module.id == module_id
        )

        if not module:
            raise ModuleNotFoundException("Module not found or unauthorized")
        
        device = await self.model.find_one(
            self.model.user_id == user_id,
            self.model.id == device_id
        )

        if not device or device.id not in module.devices:
            raise DeviceNotFoundException("Device not found or unauthorized.")
        
        return DeviceResponse(
            id=str(device.id),
            name=device.name,
            description=device.description,
            device_type=device.device_type,
            data_types=device.data_types
        )
    
    async def get_all(
        self,
        user_id: PydanticObjectId,
        module_id: PydanticObjectId
    ) -> List[DeviceResponse]:

        module = await Module.find_one(
            Module.user_id == user_id,
            Module.id == module_id
        )

        if not module:
            raise ModuleNotFoundException("Module not found or unauthorized")
        
        devices = await self.model.find(
            self.model.user_id == user_id,
            self.model.module_id == module_id
        ).to_list()

        devices_response = [
            DeviceResponse(
                id=str(device.id),
                name=device.name,
                description=device.description,
                device_type=device.device_type,
                data_types=device.data_types
            )
            for device in devices
        ]

        return devices_response
    
    async def update(self, user_id, obj_id, update_data):
        raise NotImplementedError("Update method not implemented for device class.")
    
    async def delete(
            self, 
            user_id: PydanticObjectId, 
            module_id: PydanticObjectId,
            device_id: PydanticObjectId
    ):
    
        
        module = await Module.find_one(
            Module.user_id == user_id,
            Module.id == module_id
        )

        if not module:
            raise ModuleNotFoundException("Module not found or unauthorized.")

        if device_id not in module.devices:
            raise DeviceNotFoundException("Device belongs to a different module.")
        
        device = await self.model.find_one(
            self.model.user_id == user_id,
            self.model.id == device_id
        )

        if not device:
            raise DeviceNotFoundException()
        
        await SensorReading.delete_many(SensorReading.device_id == device_id)
        await device.delete()

    async def exists(self, device_id: PydanticObjectId) -> bool:
        
        device = await self.model.find_one(
            self.model.id == device_id
        )

        if device:
            return True
        
        return False
    
    async def delete_module_devices(self, module_id: PydanticObjectId):

        await self.model.delete_many(
            self.model.module_id == module_id
        )

    async def get_by_id(self, device_id: PydanticObjectId) -> DeviceResponse:
        
        device = await self.model.find_one(
            self.model.id == device_id
        )

        return DeviceResponse(
            id=str(device.id),
            name=device.name,
            description=device.description,
            device_type=device.device_type,
            data_types=device.data_types
        )
