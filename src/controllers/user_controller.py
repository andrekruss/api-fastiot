from fastapi import APIRouter, Body, Depends, HTTPException, status

from api_requests.user_requests import CreateUserRequest
from api_responses.user_responses import UserResponse
from database.models.user_model import User
from database.repositories.user_repository import UserRepository
from exceptions.user_exceptions import UserConflictException, UserNotFoundException
from utils.auth import get_current_user
from utils.hash import hash_password

user_repository = UserRepository()
user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(create_user_request: CreateUserRequest = Body(...)):
    
    try: 
        create_user_request.password = hash_password(create_user_request.password)
        user = await user_repository.create(create_user_request)
        return user
    except UserConflictException as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )

@user_router.delete('/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: User = Depends(get_current_user)):

    try:
        await user_repository.delete(user.id)
    except UserNotFoundException as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )
    