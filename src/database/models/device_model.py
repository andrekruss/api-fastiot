from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import ConfigDict, Field

class DeviceType(str, Enum):
    SENSOR = "sensor"
    ACTUATOR = "actuator"

class Device(Document):
    user_id: PydanticObjectId
    module_id: PydanticObjectId
    name: str = Field(max_length=50)
    description: Optional[str] = Field(max_length=200)
    device_type: DeviceType
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(collection="devices", arbitrary_types_allowed=True)
