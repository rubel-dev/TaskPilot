

from fastapi import HTTPException

from app.core.security import create_access_token, hash_password, verify_password
from app.exception.custom_exceptions import UnauthorizedException
from app.models.user import User
from app.repository import user_repository


def user_create_service(user, db):
    new_user = User(
            username = user.username,
            email = user.email,
            password = hash_password(user.password)
        )  
    return user_repository.user_create(new_user = new_user, db = db)

def user_login_service(user, db):
    db_user= user_repository.user_login(user = user, db = db)
    
    if not verify_password(user.password, db_user.password):
            raise UnauthorizedException()
    token = create_access_token({
            "user_id":db_user.id
    })
    return {"access_token":token, "token_type":"bearer"}