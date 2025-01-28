from fastapi import APIRouter, Depends, HTTPException, status

from api_requests.user_requests import CreateUserRequest
from api_responses.user_responses import UserResponse
from database.models.user_model import User
from utils.auth import get_current_user
from utils.hash import hash_password

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(create_user_request: CreateUserRequest):
    
    user = await User.find_one(
        {"$or": [{"email": create_user_request.email}, {"username": create_user_request.username}]}
    )

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email or username already exists."
        )
        
    
    new_user = User(
            username=create_user_request.username,
            email=create_user_request.email,
            password=hash_password(create_user_request.password),
        )
    await new_user.insert()

    return UserResponse(
        id=str(new_user.id),
        username=new_user.username,
        email=new_user.email
    )

@user_router.get('/me', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def me(user: User = Depends(get_current_user)):
    return UserResponse(
        id=str(user.id),
        username=user.username,
        email=user.email
    )


    