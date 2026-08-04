from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from ..models.user import User, UserRole
from ..models.refresh_token import RefreshToken
from ..schemas.auth import UserCreate, UserLogin, PasswordChange, UserUpdate
from ..core.security import Security
from ..core.config import settings

class AuthService:
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        # Check if user exists
        existing_user = db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email or username already exists"
            )
        
        # Create new user
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            role=user_data.role
        )
        new_user.set_password(user_data.password)
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    
    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin) -> Dict[str, Any]:
        user = db.query(User).filter(User.email == login_data.email).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not user.verify_password(login_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        # Generate tokens
        access_token = Security.create_access_token(
            data={"sub": user.id, "email": user.email, "role": user.role.value}
        )
        refresh_token = Security.create_refresh_token(
            data={"sub": user.id}
        )
        
        # Store refresh token
        db_refresh_token = RefreshToken(
            token=refresh_token,
            user_id=user.id,
            expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(db_refresh_token)
        db.commit()
        
        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> Dict[str, Any]:
        # Validate refresh token
        stored_token = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token,
            RefreshToken.is_revoked == False
        ).first()
        
        if not stored_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        if stored_token.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired"
            )
        
        # Decode refresh token
        payload = Security.decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Create new access token
        access_token = Security.create_access_token(
            data={"sub": user.id, "email": user.email, "role": user.role.value}
        )
        
        # Create new refresh token
        new_refresh_token = Security.create_refresh_token(
            data={"sub": user.id}
        )
        
        # Store new refresh token and revoke old one
        stored_token.is_revoked = True
        
        new_stored_token = RefreshToken(
            token=new_refresh_token,
            user_id=user.id,
            expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(new_stored_token)
        db.commit()
        
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token
        }
    
    @staticmethod
    def logout(db: Session, user_id: str, refresh_token: str = None):
        if refresh_token:
            token = db.query(RefreshToken).filter(
                RefreshToken.token == refresh_token,
                RefreshToken.user_id == user_id
            ).first()
            if token:
                token.is_revoked = True
        else:
            db.query(RefreshToken).filter(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked == False
            ).update({"is_revoked": True})
        
        db.commit()
    
    @staticmethod
    def change_password(db: Session, user_id: str, password_data: PasswordChange):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.verify_password(password_data.current_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        user.set_password(password_data.new_password)
        db.commit()
    
    @staticmethod
    def update_user_profile(db: Session, user_id: str, update_data: UserUpdate) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> list:
        return db.query(User).offset(skip).limit(limit).all()
