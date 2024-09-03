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
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        # normalize path
        if path[-1] != '/':
            path += '/'
        for excluded_path in excluded_paths:
            if excluded_path[-1] != '/':
                excluded_path += '/'
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        authorization header function
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None

        return request.headers.get('Authorization')
        
    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user functiuon
        """
        return None
