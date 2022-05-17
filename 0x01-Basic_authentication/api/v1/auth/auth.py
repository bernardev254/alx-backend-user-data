#!/usr/bin/env python3
"""auth class module"""


class Auth():
    """auth class"""
    from flask import request
    from typing import List, TypeVar

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method returning a bool"""
        if path == None or excluded_paths == None or len(excluded_paths) == 0:
            return True

        if path in excluded_paths or path + "/" in excluded_paths:
            return False
        
        return True

    def authorization_header(self, request=None) -> str:
        """public method returning None"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """public method retirning None"""
        return None
