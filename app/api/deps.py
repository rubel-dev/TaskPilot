from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from app.core.database import SessionLocal

from sqlalchemy.orm import Session

from app.models.user import User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
security = HTTPBearer()
def get_current_user(
        credentials:HTTPAuthorizationCredentials = Depends(security),
        db:Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get('user_id')
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail = "Invalid Token"
            )
        user = db.query(User).filter(user_id == User.id).first()
        if user is None:
            raise HTTPException(
                status_code=404,
                detail = "User Not Found"
            )
        return user

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail = "Invalid Token"
        )