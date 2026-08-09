 

from fastapi import APIRouter, Depends, HTTPException
from app.models.refresh import RefreshToken
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_roles
from app.core.security import hash_password, hash_token, verify_password, create_access_token
from app.services.user_service import delete_user_service, update_user_role_service, user_create_service, user_login_service
router = APIRouter()

@router.post('/register')
def register(
    user:UserCreate,
    db:Session = Depends(get_db)
):
    
    return user_create_service(user = user, db= db)


@router.post('/login')
def login(
    user:UserLogin,
    db:Session = Depends(get_db)
):  
    return user_login_service(user = user, db = db)

@router.post('/logout')
def logout(
    refresh_token:str,
    db:Session = Depends(get_db)
):
    token_hash = hash_token(refresh_token)
    token_record = (
        db.query(RefreshToken).filter(RefreshToken.token_hash ==token_hash).first()

    )
    if token_record:
        token_record.revoked = True
        db.commit()

    return {
        "message":"Log out sucessfully"
    }

@router.delete('/users/{user_id}')
def delete_user(
    user_id:int,
    db:Session = Depends(get_db),
    current_user:User = Depends(require_roles(['admin']))
):
    return delete_user_service(
        db = db,
        user_id = user_id
    )

@router.patch('/users/{user_id}/role')
def update_user_role(
    user_id:int,
    role:str,
    db:Session = Depends(get_db),
    current_user:User = Depends(require_roles(['admin']))
):
    return update_user_role_service(
        db = db,
        user_id = user_id,
        role = role
    )
