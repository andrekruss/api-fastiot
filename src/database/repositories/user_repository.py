from beanie import PydanticObjectId
from api_requests.user_requests import CreateUserRequest
from api_responses.user_responses import LoginUserResponse, UserResponse
from database.models.device_model import Device
from database.models.project_model import Project
from database.models.user_model import User
from database.models.module_model import Module
from database.repositories.base_repository import BaseRepository
from exceptions.user_exceptions import UserNotFoundException
from utils.hash import hash_password

class UserRepository(BaseRepository):
    "Repository for user CRUD operations."

    def __init__(self, user_model: User):
        self.user_model = user_model

    async def get_by_id(self, user_id: PydanticObjectId, obj_id: PydanticObjectId):
        raise NotImplementedError("get_by_id method is not implemented in UserRepository class.")
    
    async def get_by_login(self, login: str) -> LoginUserResponse:

        user = await self.user_model.find_one(
            {"$or": [{"username": login}, {"email": login} ]}
        )

        if not user:
            return None
        
        return LoginUserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            password=user.password
        )

    async def get_by_email(self, email: str) -> LoginUserResponse:

        user = await self.user_model.find_one(
            self.user_model.email == email
        )

        if not user:
            return None

        return LoginUserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            password=user.password
        )
    
    async def get_by_username(self, username: str) -> LoginUserResponse:

        user = await self.user_model.find_one(
            self.user_model.username == username
        )

        if not user:
            return None

        return LoginUserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            password=user.password
        )
    
    async def create(self, user_id: PydanticObjectId, create_user_request: CreateUserRequest) -> UserResponse:
        pass
    
    async def create(self, create_user_request: CreateUserRequest) -> UserResponse:

        user = self.user_model(
            username=create_user_request.username,
            email=create_user_request.email,
            password=hash_password(create_user_request.password),
        )
        await user.insert()
        return UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email
        )

    async def update(self, user_id, obj_id, update_data):
        raise NotImplementedError("update method is not implemented in UserRepository class.")
    
    async def delete(self, user_id, obj_id):
        pass

    async def delete(self, user_id: PydanticObjectId):

        user = await self.user_model.find_one(
            self.user_model.id == user_id
        )

        if not user:
            raise UserNotFoundException()

        await Project.find(Project.user_id == user_id).delete()
        await Module.find(Module.user_id == user_id).delete()
        await Device.find(Device.user_id == user_id).delete()
        await user.delete()



    

    
    

