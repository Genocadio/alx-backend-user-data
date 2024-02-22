#!/usr/bin/env python3
"""Main file"""

import requests


def register_user(email: str, password: str) -> None:
    """
    Register a new user with the provided email and password.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        None
    """
    url = "http://localhost:5000/register"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempt to log in with the provided email and password, expecting a wrong password error.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        None
    """
    url = "http://localhost:5000/login"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Log in a user with the provided email and password.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        str: The session ID of the logged-in user.
    """
    url = "http://localhost:5000/login"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    return response.json()["session_id"]


def profile_unlogged() -> None:
    """
    Access the user profile without a valid session ID.

    Returns:
        None
    """
    url = "http://localhost:5000/profile"
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Access the user profile with a valid session ID.

    Args:
        session_id (str): The session ID of the logged-in user.

    Returns:
        None
    """
    url = "http://localhost:5000/profile"
    headers = {
        "session_id": session_id
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """
    Log out the user with the provided session ID.

    Args:
        session_id (str): The session ID of the logged-in user.

    Returns:
        None
    """
    url = "http://localhost:5000/logout"
    headers = {
        "session_id": session_id
    }
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Request a reset token for the user with the provided email.

    Args:
        email (str): The email of the user.

    Returns:
        str: The reset token for the user.
    """
    url = "http://localhost:5000/reset_password"
    data = {
        "email": email
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update the password of the user with the provided email using the reset token.

    Args:
        email (str): The email of the user.
        reset_token (str): The reset token for the user.
        new_password (str): The new password for the user.

    Returns:
        None
    """
    url = "http://localhost:5000/update_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(url, json=data)
    assert response.status_code == 200


if __name__ == "__main__":
    register_user("test@example.com", "password123")
    log_in_wrong_password("test@example.com", "wrongpassword")
    session_id = log_in("test@example.com", "password123")
    profile_unlogged()
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token("test@example.com")
    update_password("test@example.com", reset_token, "newpassword123")
