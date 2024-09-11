#!/usr/bin/env python3

"""
hash password module
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """
        Hash a password using bcrypt and return the hashed bytes.
        """
        import bcrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with email and password.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(email=email, hashed_password=hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates login credentials.
        """
        try:
            user = self._db.find_user_by(email=email)
            
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except Exception:
            return False
        
        return False


    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates if the user login is correct.

        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
        except Exception:
            return False

    def _generate_uuid() -> str:
        """
        Generate a new UUID and return its string representation.
        """
        import uuid
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """
        Creates a session for the user with the given email.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None  # User not found or error occurred

        session_id = self._generate_uuid()

        self._db.update_user(user.id, session_id=session_id)

        return session_id
