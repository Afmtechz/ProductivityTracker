"""
Configuration management for ProductivityTracker application.
Handles database, JWT, OAuth, and application settings.
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """
    Main application settings using Pydantic.
    Loads from environment variables and .env file.
    """

    # Application Info
    app_name: str = "ProductivityTracker"
    app_version: str = "1.0.0"
    debug: bool = True

    # Database Configuration
    database_url: str = "sqlite:///./test.db"
    # For PostgreSQL: postgresql://user:password@localhost/dbname

    # JWT Configuration
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Google OAuth Configuration
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/auth/google/callback"

    # CORS Configuration
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:5173",
    ]

    # Email Configuration (Optional)
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""

    # Gamification Configuration
    xp_task_completion: int = 50
    xp_habit_completion: int = 30
    xp_streak_bonus_multiplier: float = 1.5
    level_up_threshold: int = 1000

    class Config:
        """
        Pydantic config for loading environment variables.
        """
        env_file = ".env"
        case_sensitive = False
        env_file_encoding = "utf-8"


# Create global settings instance
settings = Settings()
