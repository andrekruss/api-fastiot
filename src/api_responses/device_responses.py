from typing import List, Optional
from pydantic import BaseModel

from database.models.device_model import DataType, DeviceType

class DeviceResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    device_type: DeviceType
    data_types: List[DataType]