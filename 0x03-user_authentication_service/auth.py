#!/usr/bin/env python3
"""authentication module"""
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
from db import DB
from user import User
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """password hashing method"""
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """universal unique id generator"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    @property
    def db(self) -> DB:
        """db getter"""
        return self._db

    def register_user(self, email: str, password: str) -> User:
        """register a user if not present and save to db"""
        try:
            user = self.db.find_user_by(email=email)
        except NoResultFound:
            my_hash = _hash_password(password)
            return self.db.add_user(email, my_hash)
        else:
            raise ValueError

    def valid_login(self, email: str, password: str) -> bool:
        """test for valid login"""
        try:
            user = self.db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """creates a session id and stores it in the db"""
        try:
            user = self.db.find_user_by(email=email)
            my_session_id = _generate_uuid()
            self.db.update_user(user.id, session_id=my_session_id)
            return my_session_id
        except Exception:
            pass

    def find_user_by_session_id(self, session_id: str) -> Union[User, None]:
        """find user by session id returning the user"""
        try:
            user = self.db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """session destroyer"""
        try:
            user = self.db.update(user_id, session_id=None)
            return None
        except Exception:
            pass

    def get_reset_password(self, email: str) -> str:
        """creates a reset token and stores it in the db"""
        try:
            user = self.db.find_user_by(email=email)
            my_reset_token = _generate_uuid()
            self.db.update_user(user.id, reset_token=my_reset_token)
            return my_reset_token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """updates the password using the reset password token"""
        try:
            user = self.db.find_user_by(reset_token=reset_token)
            hashed_p = self._hash_password(password)
            self.db.update_user(user.id, reset_token=None,
                                hashed_password=hashed_p)
        except Exception:
            raise ValueError
