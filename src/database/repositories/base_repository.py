from abc import ABC, abstractmethod
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel

class BaseRepository(ABC):
    """Base interface for repositories."""

    def __init__(self, model: Document):
        self.model = model

    @abstractmethod
    async def get_by_id(self, user_id: PydanticObjectId, obj_id: PydanticObjectId):
        pass

    @abstractmethod
    async def create(self, user_id: PydanticObjectId, obj_data: BaseModel):
        pass

    @abstractmethod
    async def update(self, user_id: PydanticObjectId, obj_id: PydanticObjectId, update_data: BaseModel):
        pass

    @abstractmethod
    async def delete(self, user_id:PydanticObjectId, obj_id: PydanticObjectId):
        pass
