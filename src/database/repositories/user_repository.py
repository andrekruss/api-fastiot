from beanie import PydanticObjectId
from api_requests.user_requests import CreateUserRequest
from api_responses.user_responses import LoginUserResponse, UserResponse
from database.models.device_model import Device
from database.models.module_model import Module
from database.models.project_model import Project
from database.models.sensor_reading_model import SensorReading
from database.models.user_model import User
from database.repositories.base_repository import BaseRepository
from exceptions.user_exceptions import UserConflictException, UserNotFoundException

class UserRepository(
    BaseRepository[
        User,
        UserResponse,
        CreateUserRequest,
        None
    ]
    ):
    "Repository for user CRUD operations."

    def __init__(self):
        super().__init__(User)

    async def get(self, login: str) -> UserResponse:

        user = await self.model.find_one(
            {
                "$or": {
                    {
                        "email": login
                    },
                    {
                        "username": login
                    }
                }
            }
        )

        if not user:
            raise UserNotFoundException()
        
        return UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email
        )
    
    async def get_user_login(self, login: str) -> LoginUserResponse:

        user = await self.model.find_one(
        {
            "$or": [
                {"email": login},
                {"username": login}
            ]
        }
    )

        if not user:
            raise UserNotFoundException()
        
        return LoginUserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            password=user.password
        )

    
    async def get_all(self):
        raise NotImplementedError("method get_all() not implemented for Users.")
    
    async def create(self, create_user_request: CreateUserRequest) -> UserResponse:
        
        user = await self.model.find_one(
            {
                "$or": [
                    {
                        "email": create_user_request.email
                    },
                    {
                        "username": create_user_request.username
                    }
                ]
            }
        )

        if user:
            raise UserConflictException()
        
        new_user = User(
            username=create_user_request.username,
            email=create_user_request.email,
            password=create_user_request.password,
            projects=[]
        )
        await new_user.insert()

        return UserResponse(
            id=str(new_user.id),
            username=new_user.username,
            email=new_user.email
        )
    
    async def update(self, object_id, update_object_data):
        raise NotImplementedError("method update() not implemented for Users.")
    
    async def delete(self, user_id: PydanticObjectId):

        user = await self.model.find_one(self.model.id == user_id)

        if not user:
            raise UserNotFoundException()

        if await Project.find(Project.user_id == user_id).count() > 0:
            await Project.delete_many(Project.user_id == user_id)

            if await Module.find(Module.user_id == user_id).count() > 0:
                await Module.delete_many(Module.user_id == user_id)

                if await Device.find(Device.user_id == user_id).count() > 0:
                    await Device.delete_many(Device.user_id == user_id)

                    if await SensorReading.find(SensorReading.user_id == user_id).count() > 0:
                        await SensorReading.delete_many(SensorReading.user_id == user_id)

        await user.delete()

    async def exists(self, username: str, email: str) -> bool:
        
        user = await self.model.find_one(
            {
                "$or": {
                    {
                        "username": username
                    },
                    {
                        "email": email
                    }
                }
            }
        )

        if user:
            return True
        
        return False
    



    

    
    

