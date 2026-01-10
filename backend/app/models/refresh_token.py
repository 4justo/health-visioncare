from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from .base import BaseModel
from ..core.database import Base

class RefreshToken(BaseModel, Base):
    __tablename__ = "refresh_tokens"
    
    token = Column(String(500), unique=True, nullable=False)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)
    user_agent = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)
