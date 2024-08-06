from flask import Blueprint, request, jsonify
from models import User
from utils.db import db

users = Blueprint("users", __name__)


@users.route("/", methods=["GET"])
def isAlive():
    return jsonify({"message": "Is alive"}), 400


@users.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return (jsonify({"message": "True", "user": user.serialize()}), 200)
    return (
        jsonify({"message": "User doesnt exist"}),
        404,
    )


@users.route("/user/login", methods=["POST"])
def log_in():
    body = request.get_json()
    for i in ["user", "password"]:
        if not i in body.keys() or body[i] == "" or body[i] == None:
            return (
                jsonify({"message": f"{i} is needed"}),
                400,
            )
    user_username = body.get("user")
    password = body.get("password")
    user = User.query.filter_by(username=user_username).first()
    if user:
        if password == user.password:
            return (
                jsonify(
                    {
                        "message": "True",
                        "id": user.id,
                        "name": user.name.capitalize(),
                        "surname": user.surname.capitalize(),
                        "username": user.username,
                        "avatar": user.avatar,
                    }
                ),
                200,
            )
        return (jsonify({"message": "False"}), 200)
    return (
        jsonify({"message": "User doesnt exist"}),
        404,
    )


@users.route("/user", methods=["POST"])
def create_user():
    body = request.get_json()
    for i in ["surname", "password", "name", "username"]:
        if not i in body.keys() or body[i] == "" or body[i] == None:
            return (
                jsonify({"message": f"{i} is needed"}),
                400,
            )
    avatar = body.get("avatar")
    name = body.get("name").capitalize()
    surname = body.get("surname").capitalize()
    username = body.get("username").lower()
    password = body.get("password")
    possible_user = User.query.filter_by(username=username).first()
    if possible_user:
        return jsonify({"message": f"User {username} already exists"}), 422
    if len(password) < 5 or len(password) > 10:
        return (
            jsonify({"message": "Password must be between 5 and 10 characters long"}),
            400,
        )
    if avatar != None and len(avatar) > 200:
        return (jsonify({"message": "Avatar must be 200 characters maximum"}), 400)
    for i in [name, surname, username]:
        if len(i) < 3 or len(i) > 20:
            return (
                jsonify({"message": f"Name must be between 3 and 20 characters long"}),
                400,
            )
    user = User(
        name=name,
        surname=surname,
        username=username,
        avatar=avatar,
        password=password,
    )
    db.session.add(user)
    db.session.commit()
    return (
        jsonify({"message": "A user has been created", "user": user.id}),
        201,
    )
