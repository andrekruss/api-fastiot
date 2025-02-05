from typing import Optional
from pydantic import BaseModel

from database.models.device_model import DeviceType

class CreateDeviceRequest(BaseModel):
    name: str
    description: Optional[str]
    device_type: DeviceType