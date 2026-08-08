 

from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.services.user_service import user_create_service, user_login_service
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