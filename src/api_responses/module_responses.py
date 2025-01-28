from typing import Optional
from pydantic import BaseModel

class ModuleResponse(BaseModel):
    id: str
    user_id: str
    project_id: str
    name: str
    description: Optional[str]