import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth

class SessionExpAuth(SessionAuth):
    """SessionAuth with expiration logic."""

    def __init__(self):
        """Initialize the class with session duration."""
        super().__init__()
        try:
            # Set session duration from environment variable
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            # If SESSION_DURATION is invalid, set to 0
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session with an expiration."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_info = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_info
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve the user_id considering expiration."""
        if session_id is None:
            return None

        session_info = self.user_id_by_session_id.get(session_id)
        if session_info is None:
            return None

        if self.session_duration <= 0:
            return session_info.get("user_id")

        created_at = session_info.get("created_at")
        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None

        return session_info.get("user_id")

