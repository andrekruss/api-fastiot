from typing import List, Optional
from pydantic import BaseModel

from enums.data_type import DataType
from enums.device_type import DeviceType

class CreateDeviceRequest(BaseModel):
    name: str
    description: Optional[str]
    device_type: DeviceType
    data_types: List[DataType]