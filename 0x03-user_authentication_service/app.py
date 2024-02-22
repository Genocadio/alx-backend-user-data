#!/usr/bin/env python3
""" Flask app module
"""
from flask import Flask, request, jsonify, abort
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


@app.route('/sessions/<session_id>', methods=['DELETE'], strict_slashes=False)
def logout(session_id: str) -> str:
    """DELETE /sessions/<session_id>
    Return: {"message": "Bienvenue"}
    """
    auth = Auth()
    if not auth.destroy_session(session_id):
        abort(403)
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
