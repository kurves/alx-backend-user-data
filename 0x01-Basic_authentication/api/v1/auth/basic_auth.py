#!/usr/bin/env python3

"""
Basic Auth module
"""

from api.v1.auth.auth import Auth


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
