from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from utils.token import decode_jwt_token
from database.models.user_model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    email = decode_jwt_token(token)
    user = await User.find_one({"email": email})
    return user
    
    