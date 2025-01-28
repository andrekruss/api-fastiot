from passlib.hash import pbkdf2_sha256

def hash_password(plain_password: str) -> str:
    return pbkdf2_sha256.hash(plain_password)

def verify_password(plain_password: str, hash: str) -> bool:
    return pbkdf2_sha256.verify(plain_password, hash)