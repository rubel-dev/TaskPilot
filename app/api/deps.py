from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from app.core.database import SessionLocal

from sqlalchemy.orm import Session

from app.exception.custom_exceptions import ForbiddenException
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

# def require_admin(
#         current_user:User = Depends(get_current_user)
# ):
#     if current_user.role != 'admin':
#         raise ForbiddenException("Admin access required")
#     return current_user

# def require_manager(
#         current_user:User = Depends(get_current_user)
# ):
#     if current_user.role != 'manager':
#         raise ForbiddenException("Manager access required")
#     return current_user

# def require_user(
#         current_user:User = Depends(get_current_user)
# ):
#     if current_user.role != 'user':
#         raise ForbiddenException("User access required")
#     return current_user


# def require_role(required_role):
#     def check_role(
#             current_user:User = get_current_user()
#     ):
#         if current_user.role != require_role:
#             raise ForbiddenException("Insufficient Permission")
#         return current_user
#     return check_role


def require_roles(allowed_roles:list[str]):
    def checker(
            current_user:User = Depends(get_current_user)
    ):
        if current_user.role not in allowed_roles:
            raise ForbiddenException("Insufficent Permission")
        return current_user
    return checker