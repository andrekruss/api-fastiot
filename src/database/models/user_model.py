from datetime import datetime, timezone
from beanie import Document, before_event, Replace
from pydantic import ConfigDict, Field, EmailStr
from typing import List

class User(Document):
    username: str = Field(max_length=30, json_schema_extra={"unique": True})
    email: EmailStr = Field(json_schema_extra={"unique": True})
    password: str = Field(max_length=256)  
    projects: List[str] = Field(default_factory=list)  
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @before_event(Replace)
    def update_timestamp(self):
        """Updates the updated_at timestamp before saving"""
        self.updated_at = datetime.now(timezone.utc)
