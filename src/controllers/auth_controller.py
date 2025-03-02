from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from database.models.user_model import User
from utils.token import generate_jwt_token
from utils.hash import verify_password
from database.repositories.user_repository import UserRepository
from api_responses.auth_responses import TokenResponse

user_repository = UserRepository(User)
auth_router = APIRouter(tags=["auth"])

@auth_router.post('/token', status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def login(login_form_data: OAuth2PasswordRequestForm = Depends()):

    user = await user_repository.get_by_login(login_form_data.username)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email or username not registered.")

    if not verify_password(login_form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect user or password.")
    
    jwt_token = generate_jwt_token({"sub": user.email})
    return TokenResponse(access_token=jwt_token, token_type="bearer")