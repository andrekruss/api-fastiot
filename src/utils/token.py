from datetime import datetime, timedelta, timezone
import jwt

from app_secrets import JWT_SECRET_KEY, ALGORITHM, EXPIRATION_TIME

def generate_jwt_token(data: dict) -> str:
    data_to_encode = data.copy()
    data_to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME)})
    token = jwt.encode(data_to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_jwt_token(encoded_token: str) -> str:
    decoded_data = jwt.decode(encoded_token, JWT_SECRET_KEY, algorithms=["HS256"])
    return decoded_data["sub"] # returns email encoded on payload


    