from datetime import datetime, timezone
from typing import List, Optional
from beanie import Document, PydanticObjectId, Replace, before_event
from pydantic import ConfigDict, Field

class Module(Document):
    user_id: PydanticObjectId
    project_id: PydanticObjectId
    name: str = Field(max_length=50)
    description: Optional[str] = Field(max_length=200)
    devices: List[PydanticObjectId] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @before_event(Replace)
    def update_timestamp(self):
        """Updates the updated_at timestamp before saving"""
        self.updated_at = datetime.now(timezone.utc)