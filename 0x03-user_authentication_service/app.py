#!/usr/bin/env python3
""" Flask app module
"""
from flask import Flask, request, jsonify
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
