
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey

from app.core.database import Base


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token_hash = Column(String, unique = True, nullable=False)
    expires_at = Column(DateTime, nullable = False)
    revoked = Column(Boolean, default=False)
    
    