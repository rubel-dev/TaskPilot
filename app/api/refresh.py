from datetime import datetime, timedelta, timezone

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import create_access_token, hash_token
from app.exception.custom_exceptions import UnauthorizedException
from app.models.refresh import RefreshToken

router = APIRouter()
@router.post('/refresh')
def refresh(
        refresh_token:str,
        db: Session = Depends(get_db)
):
    token_hash = hash_token(refresh_token)
    token_record =( db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash
    ).first())
    if not token_record:
        raise UnauthorizedException("Invalid refrsh token")
    if token_record.revoked:
        raise UnauthorizedException("Refresh token revoked")
    if token_record.expires_at < datetime.now(timezone.utc):
        raise UnauthorizedException("Refresh token expired")
    
    token_record.revoked = True
    new_access_token = create_access_token(
        {
            "user_id":token_record.user_id
        }
    )
    new_refresh_token = create_access_token()
    new_record = RefreshToken(
        user_id = token_record.user_id,
        token_hash = hash_token(new_refresh_token),
        expires_at = datetime.now(timezone.utc) + timedelta(days = 7),
        revoked=False
    )
    db.add(new_record)
    db.commit()
    return {
        "access_token":new_access_token,
        "refresh_token":new_refresh_token,
        "token_type":"bearer",
    }