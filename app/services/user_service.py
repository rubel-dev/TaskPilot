

from datetime import UTC, datetime, timedelta

from fastapi import HTTPException

from app.core.security import create_access_token, create_refresh_token, hash_password, hash_token, verify_password
from app.exception.custom_exceptions import InvalidCredentialsException, NotFoundException, UnauthorizedException
from app.models.refresh import RefreshToken
from app.models.user import User
from app.repository import user_repository


def user_create_service(user, db):
    new_user = User(
            username = user.username,
            email = user.email,
            password = hash_password(user.password),
            role = user.role
        )  
    return user_repository.user_create(new_user = new_user, db = db)

def user_login_service(user, db):
    db_user= user_repository.user_login(user = user, db = db)
    
    if not verify_password(user.password, db_user.password):
            raise UnauthorizedException()
    token = create_access_token({
            "user_id":db_user.id,
            "role":db_user.role
    })

    refresh_token = create_refresh_token()
    refresh_record = RefreshToken(
         user_id = db_user.id,
         token_hash = hash_token(refresh_token),
         expires_at=datetime.now(UTC) + timedelta(days = 7),
         revoked = False,
    )
    user_repository.user_login_refresh(refresh_record=refresh_record, db = db)
    return {
         "access_token":token, 
         "refresh_token":refresh_token,
         "token_type":"bearer"
         }

def delete_user_service(db, user_id):
     user = db.query(User).filter(User.id == user_id).filter()
     if not user:
          raise NotFoundException("user not found")
     db.delete(user)
     db.commit()

def update_user_role_service(db, user_id, role):
     user = db.query(User).filter(User.id == user_id).filter().first()
     if not user:
          raise NotFoundException("user not found")
     if role not in ["admin", "manager", "user"]:
          raise InvalidCredentialsException("Invalid role")
     user.role = role
     db.commit()
     db.refresh(user)
     return user
