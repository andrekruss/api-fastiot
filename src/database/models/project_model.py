from beanie import Document, PydanticObjectId, before_event, Replace
from pydantic import ConfigDict, Field
from typing import Optional, List
from datetime import datetime, timezone

class Project(Document):
    user_id: PydanticObjectId
    name: str = Field(max_length=50)
    description: Optional[str] = Field(max_length=200)
    modules: List[PydanticObjectId] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(collection="projects", arbitrary_types_allowed=True)

    @before_event(Replace)
    def update_timestamp(self):
        """Updates the updated_at timestamp before saving"""
        self.updated_at = datetime.now(timezone.utc)