from datetime import datetime
from typing import Any
from pydantic import BaseModel

from enums.data_type import DataType

class SensorReadingResponse(BaseModel):
    id: str
    data_type: DataType
    value: Any
    created_at: datetime