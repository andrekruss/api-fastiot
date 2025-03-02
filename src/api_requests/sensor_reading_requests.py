from typing import Any
from beanie import PydanticObjectId
from pydantic import BaseModel

from enums.data_type import DataType

class CreateReadingRequest(BaseModel):
    device_id: PydanticObjectId
    data_type: DataType
    value: Any