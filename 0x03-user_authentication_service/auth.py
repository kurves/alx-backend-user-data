#!/usr/bin/env python3

"""
hash password module
"""

import bcrypt
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hashes the given password using bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed_password

def register_user(self, email: str, password: str) -> User:
        """
        Registers a user with the provided email and password.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user
