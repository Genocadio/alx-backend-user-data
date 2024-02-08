#!/usr/bin/env python3
'''Password Hashing module'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''hash pass function'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
