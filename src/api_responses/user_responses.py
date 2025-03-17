from typing import Optional
from pydantic import BaseModel

class LoginUserResponse(BaseModel):
    id: str
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
