from abc import ABC, abstractmethod
from typing import Generic, List, Optional, Type, TypeVar
from beanie import Document, PydanticObjectId
from pydantic import BaseModel

DATABASE_MODEL = TypeVar("MODEL", bound=Document)
RESPONSE_DTO = TypeVar("RESPONSE_DTO", bound=BaseModel)
CREATE_OBJECT_DTO = TypeVar("CREATE_OBJECT_DTO", bound=BaseModel)
UPDATE_OBJECT_DTO = TypeVar("UPDATE_OBJECT_DTO", bound=BaseModel)

class BaseRepository(ABC, Generic[DATABASE_MODEL, RESPONSE_DTO, CREATE_OBJECT_DTO, UPDATE_OBJECT_DTO]):
    """Base interface for repositories."""

    def __init__(self, model: Type[DATABASE_MODEL]):
        self.model = model

    @abstractmethod
    async def get(self, object_id: PydanticObjectId) -> RESPONSE_DTO:
        pass

    @abstractmethod
    async def get_all(self) -> List[RESPONSE_DTO]:
        pass

    @abstractmethod
    async def create(self, create_object_data: CREATE_OBJECT_DTO) -> RESPONSE_DTO:
        pass

    @abstractmethod
    async def update(self, object_id: PydanticObjectId, update_object_data: UPDATE_OBJECT_DTO) -> Optional[RESPONSE_DTO]:
        pass
    
    @abstractmethod
    async def delete(self, object_id: PydanticObjectId):
        pass

    @abstractmethod
    async def exists(self, object_id: PydanticObjectId) -> bool:
        pass
