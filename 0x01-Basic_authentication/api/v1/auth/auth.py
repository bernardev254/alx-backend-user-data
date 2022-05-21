#!/usr/bin/env python3
"""auth class module"""


class Auth():
    """auth class"""
    from flask import request
    from typing import List, TypeVar

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method returning a bool"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        for my_path in excluded_paths:
            if my_path[-1] is "*":
                if my_path[:-2] in path:
                    return False

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
