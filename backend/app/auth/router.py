"""
Authentication API routes.
Handles user registration, login, token management, and OAuth.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from .models import User
from .schemas import (
    UserRegister, UserLogin, TokenResponse, GoogleLoginRequest,
    RefreshTokenRequest, UserProfile
)
from .jwt_handler import (
    hash_password, verify_password, create_access_token, 
    create_refresh_token, verify_token
)
from .google_oauth import GoogleOAuthHandler
from ..validators import validate_email, validate_password
from ..dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user with email and password.

    Args:
        user_data: Registration data (email, password, full_name)
        db: Database session

    Returns:
        Token response with access and refresh tokens

    Raises:
        HTTPException: If email already exists or validation fails
    """
    # Validate email format
    if not validate_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Validate password strength
    is_valid, error_msg = validate_password(user_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )

    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        full_name=user_data.full_name or "",
        is_verified=False
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Create tokens
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 1800  # 30 minutes
    }


@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password.

    Args:
        user_data: Login credentials
        db: Database session

    Returns:
        Token response with access and refresh tokens

    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by email
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Update last login
    user.last_login_at = datetime.utcnow()
    db.commit()

    # Create tokens
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 1800
    }


@router.post("/google", response_model=TokenResponse)
def google_login(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    """
    Login or register with Google OAuth token.

    Args:
        request: Google token
        db: Database session

    Returns:
        Token response

    Raises:
        HTTPException: If token is invalid
    """
    # Verify Google token
    google_data = GoogleOAuthHandler.verify_token(request.token)
    if not google_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token"
        )

    # Try to find existing user
    user = db.query(User).filter(User.google_id == google_data["google_id"]).first()

    if not user:
        # Try to find by email (for existing email/password users)
        user = db.query(User).filter(User.email == google_data["email"]).first()
        if not user:
            # Create new user
            user = User(
                email=google_data["email"],
                full_name=google_data["full_name"],
                google_id=google_data["google_id"],
                profile_picture_url=google_data["profile_picture_url"],
                is_verified=google_data["email_verified"]
            )
            db.add(user)
        else:
            # Link existing user to Google
            user.google_id = google_data["google_id"]
            if google_data["profile_picture_url"]:
                user.profile_picture_url = google_data["profile_picture_url"]
    else:
        # Update profile picture if changed
        if google_data["profile_picture_url"]:
            user.profile_picture_url = google_data["profile_picture_url"]

    # Update last login
    user.last_login_at = datetime.utcnow()
    user.is_verified = True  # Google verified

    db.commit()
    db.refresh(user)

    # Create tokens
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 1800
    }


@router.post("/refresh", response_model=TokenResponse)
def refresh_access_token(request: RefreshTokenRequest):
    """
    Refresh access token using refresh token.

    Args:
        request: Refresh token

    Returns:
        New access token

    Raises:
        HTTPException: If refresh token is invalid
    """
    user_id = verify_token(request.refresh_token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    # Create new access token
    access_token = create_access_token(data={"sub": user_id})
    refresh_token = create_refresh_token(data={"sub": user_id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 1800
    }


@router.get("/google/url")
def get_google_oauth_url():
    """
    Get Google OAuth authorization URL.

    Returns:
        OAuth URL for frontend redirect
    """
    url = GoogleOAuthHandler.get_oauth_url()
    return {"url": url}


@router.get("/me", response_model=UserProfile)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user's profile.

    Args:
        current_user: Current authenticated user

    Returns:
        User profile information
    """
    return current_user


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """
    Logout user (token invalidation on client side).

    Args:
        current_user: Current authenticated user

    Returns:
        Logout confirmation
    """
    return {"message": "Logged out successfully"}
