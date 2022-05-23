#!/usr/bin/env python3
"""authentication module"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """password hashing method"""
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed
