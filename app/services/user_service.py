

from fastapi import HTTPException

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User


def user_create_service(user, db):
    new_user = User(
            username = user.username,
            email = user.email,
            password = hash_password(user.password)
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def user_login_service(user, db):
    db_user= db.query(User).filter(User.email == user.email).first()
    
    if not verify_password(user.password, db_user.password):
            raise HTTPException(
                status_code=404,
                detail = "invalid authentication"
            )
    token = create_access_token({
            "user_id":db_user.id
    })
    return {"access_token":token, "token_type":"bearer"}