from typing import Optional
from pydantic import BaseModel

class CreateModuleRequest(BaseModel):
    name: str
    description: Optional[str]