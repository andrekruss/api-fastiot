from datetime import datetime, timezone
from typing import List, Optional
from beanie import Document, Replace, before_event
from bson import ObjectId
from pydantic import ConfigDict, Field

class Module(Document):
    project_id: ObjectId
    name: str = Field(max_length=50)
    description: Optional[str] = Field(max_length=200)
    devices: List[ObjectId] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(collection="modules", arbitrary_types_allowed=True)

    @before_event(Replace)
    def update_timestamp(self):
        """Updates the updated_at timestamp before saving"""
        self.updated_at = datetime.now(timezone.utc)