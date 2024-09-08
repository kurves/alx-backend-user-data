#!/usr/bin/env python3

"""
Session in atabase odule
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from models import storage

class SessionDBAuth(SessionExpAuth):
    """Session-based authentication with sessions"""

    def create_session(self, user_id=None):
        """Create and store a new session in the database."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user_id from database using session_id."""
        if session_id is None:
            return None

        sessions = storage.all(UserSession)
        for session in sessions.values():
            if session.session_id == session_id:
                return session.user_id

        return None

    def destroy_session(self, request=None):
        """Destroy the session based on the session ID"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        sessions = storage.all(UserSession)
        for session_key, session in sessions.items():
            if session.session_id == session_id:
                session.delete()
                storage.save()
                return True

        return False

