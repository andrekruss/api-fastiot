from typing import List, Optional
from pydantic import BaseModel, Field

class ModuleResponse(BaseModel):
    id: str
    user_id: str
    project_id: str
    name: str
    description: Optional[str]
    devices: Optional[List[str]] = Field(default_factory=list)
