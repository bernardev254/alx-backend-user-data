#!/usr/bin/env python3
"""basic_auth class module"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import List, TypeVar
from flask import request


class BasicAuth(Auth):
    """auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method returning a bool"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path in excluded_paths or path + "/" in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """public method returning None"""
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """public method retirning None"""
        return None

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """method returning authorization header"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """returns a decoded authorization string"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            validencode = base64_authorization_header.encode('utf-8')
            validecode = b64decode(validencode)
            string = validecode.decode('utf-8')
            return string
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """returns the user email and password
           from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        autho = decoded_base64_authorization_header.split(":", 1)
        return autho[0], autho[1]

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd:
                                     str) -> TypeVar('User'):
        """
           that returns the User instance based on his email and password
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            users = User.search({"email": user_email})
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns the User object"""
        try:
            header = self.authorization_header(request)
            string = self.extract_base64_authorization_header(header)
            autho = self.decode_base64_authorization_header(string)
            creds = self.extract_user_credentials(auth0)
            user = self.user_object_from_credentials(creds[0], creds[1])
            return user
        except Exception:
            return None
