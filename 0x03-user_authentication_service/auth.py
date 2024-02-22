#!/user/bin/env python3
""" authentication module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    method to hash a password and return the hashed password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password
