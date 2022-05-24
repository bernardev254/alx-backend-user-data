#!/usr/bin/env python3
"""Basic flask app"""

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index() -> str:
    """root route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """users route"""
    my_email = request.form['email']
    pwd = request.form['password']
    try:
        AUTH.register_user(my_email, pwd)
        return jsonify({"email": my_email,
                       "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
