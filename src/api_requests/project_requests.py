from pydantic import BaseModel
from typing import Optional

class CreateProjectRequest(BaseModel):
    name: str
    description: Optional[str] = None

class PatchProjectRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
