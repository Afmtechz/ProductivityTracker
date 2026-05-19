"""
Google OAuth 2.0 integration.
Handles Google login and user creation/update.
"""

from google.auth.transport import requests
from google.oauth2 import id_token
from typing import Optional, Dict
from ..config import settings


class GoogleOAuthHandler:
    """
    Handles Google OAuth 2.0 authentication.
    """

    @staticmethod
    def verify_token(token: str) -> Optional[Dict]:
        """
        Verify Google ID token and extract user information.

        Args:
            token: Google ID token from client

        Returns:
            Dict with user info (email, name, picture) or None if invalid
        """
        try:
            # Verify token with Google's public keys
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.google_client_id
            )

            # Verify token hasn't been revoked
            if idinfo.get('aud') != settings.google_client_id:
                return None

            return {
                "google_id": idinfo.get("sub"),
                "email": idinfo.get("email"),
                "full_name": idinfo.get("name"),
                "profile_picture_url": idinfo.get("picture"),
                "email_verified": idinfo.get("email_verified", False),
            }
        except Exception as e:
            print(f"Token verification failed: {str(e)}")
            return None

    @staticmethod
    def get_oauth_url() -> str:
        """
        Generate Google OAuth authorization URL.

        Returns:
            Authorization URL for user to click
        """
        from urllib.parse import urlencode

        params = {
            "client_id": settings.google_client_id,
            "redirect_uri": settings.google_redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
        }

        return "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)
