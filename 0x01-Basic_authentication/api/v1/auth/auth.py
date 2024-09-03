#!/usr/bin/env python3

"""
Authentication module
"""

from flask import request


"""
Authrntication clss
"""

class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        require authentication function
        """


    def authorization_header(self, request=None) -> str:
        """
        authorization header function
        """

   def current_user(self, request=None) -> TypeVar('User'):
       """

   

