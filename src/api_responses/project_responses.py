from pydantic import BaseModel, Field
from typing import Optional, List

class ProjectResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: str
    modules: Optional[List[str]] = Field(default_factory=list)
