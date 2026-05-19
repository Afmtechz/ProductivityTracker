"""
Pydantic schemas for authentication endpoints.
Used for request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserRegister(BaseModel):
    """
    Schema for user registration.
    """
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123",
                "full_name": "John Doe"
            }
        }


class UserLogin(BaseModel):
    """
    Schema for user login.
    """
    email: EmailStr
    password: str = Field(..., min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123"
            }
        }


class TokenResponse(BaseModel):
    """
    Schema for token response.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # Seconds

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800
            }
        }


class GoogleLoginRequest(BaseModel):
    """
    Schema for Google OAuth login.
    """
    token: str = Field(..., description="Google ID token from client")


class RefreshTokenRequest(BaseModel):
    """
    Schema for token refresh.
    """
    refresh_token: str


class UserProfile(BaseModel):
    """
    Schema for user profile response.
    """
    id: int
    email: str
    full_name: Optional[str]
    profile_picture_url: Optional[str]
    bio: Optional[str]
    theme: str
    is_active: bool
    created_at: datetime
    last_login_at: Optional[datetime]

    class Config:
        from_attributes = True


class PasswordChangeRequest(BaseModel):
    """
    Schema for password change.
    """
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str
