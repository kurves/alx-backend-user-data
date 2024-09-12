#!/usr/bin/env python3

"""
hash password module
"""

import bcrypt
from db import DB
from user import User
from typing import Optional
from sqlalchemy.orm.exc import NoResultFound

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """
        Initialize a db instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user if the email does not already exist.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pw = self._hash_password(password)
            user = self._db.add_user(email, hashed_pw)
            return user

    def _hash_password(self, password: str) -> bytes:
        """
        Hash a password using bcrypt and return the hashed bytes.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates login credentials.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
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
