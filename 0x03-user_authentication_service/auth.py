#!/usr/bin/env python3
"""authentication module"""
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """password hashing method"""
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed


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

    def _generate_uuid(self) -> str:
        """uuid generator"""
        import uuid

        return uuid.uuid4()

    def create_session(self, email: str) -> str:
        """creates a session id and stores it in the db"""
        try:
            user = self.db.find_user_by(email=email)
            my_session_id = self._generate_uuid()
            self.db.update_user(user.id, session_id=my_session_id)
            return my_session_id
        except Exception:
            pass
