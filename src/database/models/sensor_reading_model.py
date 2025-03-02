from datetime import datetime, timezone
from typing import Any
from beanie import Document, PydanticObjectId
from pydantic import ConfigDict, Field

from enums.data_type import DataType

class SensorReading(Document):
    user_id: PydanticObjectId
    device_id: PydanticObjectId
    value: Any
    data_type: DataType
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(arbitrary_types_allowed=True)