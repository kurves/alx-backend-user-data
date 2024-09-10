#!/usr/bin/env python3
"""
user model module
"""


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound, InvalidRequestError
from typing import Dict
from user import Base
from user import User

class DB:
    """
    DB class for interacting with the database.
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance and create the necessary tables.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object for database interactions.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user in the database using arbitrary keyword.
        """
        if not kwargs:
            raise InvalidRequestError("No arguments provided for query")

        try:
            return self._session.query(User).filter_by(**kwargs).first()
        except NoResultFound:
            raise NoResultFound("No user found with the specified attributes")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid request, check the query arguments")

     def update_user(self, user_id: int, **kwargs: Dict) -> None:
        """
        try:
            user = self.find_user_by(id=user_id)

            for key, value in kwargs.items():
                if not hasattr(user, key):
                    raise ValueError(f"Invalid attribute: {key}")
                setattr(user, key, value)

            self._session.commit()

        except NoResultFound:
            raise ValueError(f"No user found with id: {user_id}")
        except InvalidRequestError as e:
            raise ValueError(f"Error during update: {str(e)}")
