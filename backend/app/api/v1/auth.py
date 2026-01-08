from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from ...core.database import get_db
from ...core.auth import get_current_user, get_current_admin_user, require_role
from ...services.auth_service import AuthService
from ...schemas.auth import (
    UserCreate, UserLogin, Token, TokenRefresh, UserResponse,
    UserUpdate, PasswordChange, LoginResponse
)
from ...models.user import User

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    user = AuthService.register_user(db, user_data)
    return user

@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    """Login user and get tokens"""
    result = AuthService.authenticate_user(db, login_data)
    
    return LoginResponse(
        user=result["user"],
        access_token=result["access_token"],
        refresh_token=result["refresh_token"]
    )

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: TokenRefresh,
    db: Session = Depends(get_db)
):
    """Refresh access token"""
    result = AuthService.refresh_access_token(db, refresh_data.refresh_token)
    return Token(
        access_token=result["access_token"],
        refresh_token=result["refresh_token"]
    )

@router.post("/logout")
async def logout(
    refresh_token: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout user and revoke tokens"""
    AuthService.logout(db, current_user.id, refresh_token)
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information"""
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    user = AuthService.update_user_profile(db, current_user.id, update_data)
    return user

@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    AuthService.change_password(db, current_user.id, password_data)
    return {"message": "Password changed successfully"}

# Admin endpoints
@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    users = AuthService.get_users(db, skip, limit)
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    current_user: User = Depends(require_role(["admin", "doctor"])),
    db: Session = Depends(get_db)
):
    """Get user by ID (admin/doctor only)"""
    user = AuthService.get_user_by_id(db, user_id)
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    update_data: UserUpdate,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Update user (admin only)"""
    user = AuthService.update_user_profile(db, user_id, update_data)
    return user

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    """Delete user (admin only) - soft delete"""
    user = AuthService.get_user_by_id(db, user_id)
    user.is_active = False
    db.commit()
    return {"message": "User deactivated successfully"}
