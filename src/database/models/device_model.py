from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, ConfigDict, Field

from enums.data_type import DataType
from enums.device_type import DeviceType


class Device(Document):
    user_id: PydanticObjectId
    module_id: PydanticObjectId
    name: str = Field(max_length=50)
    description: Optional[str] = Field(max_length=200)
    device_type: DeviceType
    data_types: List[DataType]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(arbitrary_types_allowed=True)
