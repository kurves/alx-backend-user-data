#!/usr/bin/env python3

"""
Basic Auth module
"""

from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar, Optional
from models.user import User


class BasicAuth(Auth):
    """
    Basic auth class inherits auth class
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts the BAse 64 Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decodes a Base64 string to a UTF-8 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Extracts user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        user_email, user_password = decoded_base64_authorization_header.split(':', 1)
        return user_email, user_password

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> Optional[TypeVar('User')]:
        """
        Returns the User instance based on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        
        if not users:
            return None
        
        user = users[0]
        
        if not user.is_valid_password(user_pwd):
            return None
        
        return user


    def current_user(self, request=None) -> Optional[TypeVar('User')]:
        """
        Retrieves the User  using Basic Authentication
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        
        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None
        
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if decoded_auth is None:
            return None
        
        user_email, user_pwd = self.extract_user_credentials(decoded_auth)
        if user_email is None or user_pwd is None:
            return None
        
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
