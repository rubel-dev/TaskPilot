from passlib.context import CryptContext
from jose import JWTError, jwt
from app.core.config import SECRET_KEY, ALGORITHM
from datetime import UTC, datetime, timedelta
import secrets
import hashlib

pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated = "auto"
)

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

# SECRET_KEY = "supersecretkey"
# ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "type":"access",
        "exp":expire
        })
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm = ALGORITHM
    )
    return encoded_jwt

def create_refresh_token():
    return secrets.token_urlsafe(64)

def hash_token(token:str):
    return hashlib.sha256(
        token.encode()
    ).hexdigest()