#!/usr/bin/env python3
""" Flask app module
"""
from flask import Flask, request, jsonify, abort, redirect
from auth import Auth


app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """GET /
    Return: {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """POST /users
    JSON body:
      - email: string
      - password: string
    Return: {"email": email, "message": "user created"}
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None or password is None:
        return jsonify({"message": "email and password required"}), 400
    try:
        auth = Auth()
        new_user = auth.register_user(email, password)
        return jsonify({"email": new_user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """POST /sessions
    Return:
        - JSON payload of the form containing login info.
    """
    auth = Auth()
    email, password = request.form.get("email"), request.form.get("password")
    if not auth.valid_login(email, password):
        abort(401)
    session_id = auth.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """DELETE /sessions
    Return:
        - Redirect to GET / if session is destroyed.
        - 403 HTTP status if session does not exist.
    """
    auth = Auth()
    session_id = request.cookies.get("session_id")
    user = auth.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    auth.destroy_session(user.id)
    return redirect("/")


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """GET /profile
    Return:
        - JSON payload of the form containing user profile info.
    """
    session_id = request.cookies.get("session_id")
    auth = Auth()
    user = auth.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """POST /reset_password
    Return:
        - JSON payload of the form containing reset password token.
    """
    email = request.form.get("email")
    auth = Auth()
    try:
        token = auth.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """PUT /reset_password
    Return:
        - JSON payload of the form containing update password info.
    """
    email = request.form.get("email")
    token = request.form.get("reset_token")
    password = request.form.get("new_password")
    auth = Auth()
    try:
        auth.update_password(token, password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
