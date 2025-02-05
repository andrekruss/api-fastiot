from typing import Optional
from pydantic import BaseModel

from database.models.device_model import DeviceType

class DeviceResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    device_type: DeviceType