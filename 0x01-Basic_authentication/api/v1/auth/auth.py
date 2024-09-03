#!/usr/bin/env python3

"""
Authentication module
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        require authentication function
        """
        return False


    def authorization_header(self, request=None) -> str:
        """
        authorization header function
        """
        return None


    def current_user(self, request=None) -> TypeVar('User'):
       """
       current user functiuon
       """
       return None
