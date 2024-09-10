#!/usr/bin/env python3

"""
hash password module
"""

import bcrypt

def _hash_password(password: str) -> bytes:
    """
    Hashes the given password using bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed_password
