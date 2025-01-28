from datetime import datetime, timezone
from beanie import Document, before_event, Replace
from pydantic import Field, EmailStr
from typing import List

class User(Document):
    username: str = Field(max_length=30, unique=True)
    email: EmailStr = Field(unique=True)
    password: str = Field(max_length=256)  
    projects: List[str] = Field(default_factory=list)  # projects ids
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"

    @before_event(Replace)
    def update_timestamp(self):
        """Updates the updated_at timestamp before saving"""
        self.updated_at = datetime.now(timezone.utc)
