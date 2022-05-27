#!/usr/bin/env python3
"""Basic flask app"""

from flask import Flask, jsonify, request, make_response, abort
from flask import url_for, redirect
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


@app.route("/sessions", methods=["POST", "DELETE"], strict_slashes=False)
def login() -> str:
    """respond to session route and validates login"""
    if request.method == "DELETE":
        my_session_id = request.cookies.get("session_id")
        try:
            user = AUTH.find_user_by_session_id(session_id=my_session_id)
            AUTH.destroy_session(user.user_id)
            return redirect(url_for("index"))
        except Exception:
            abort(403)
    email = request.form['email']
    password = request.form['password']
    if AUTH.valid_login(email, password):
        my_session_id = AUTH.create_session(email)
        out = jsonify({"email": email,
                      "message": "logged in"})
        resp = make_response(out)
        resp.set_cookie("session_id", my_session_id)
        return resp
    abort(401)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def user_profile() -> str:
    """my user profile"""
    my_session_id = request.cookies.get('session_id')
    try:
        user = AUTH.db.find_user_by(session_id=my_session_id)
        return jsonify({"email": user.email}), 200
    except Exception:
        return jsonify({"my_session_id": my_session_id})
        #return jsonify({"user.session_id": user.session_id})
        #abort(403)
   

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
