from flask import Blueprint, request, jsonify
from models import Post, User
from utils.db import db

posts = Blueprint("posts", __name__)


@posts.route("/post", methods=["POST"])
def create_post():
    body = request.get_json()
    for i in ["image", "message", "author", "location", "status"]:
        if not i in body.keys() or body[i] == "" or body[i] == None:
            return (
                jsonify({"message": f"{i} is needed"}),
                400,
            )
    image = body.get("image")
    message = body.get("message").capitalize()
    author = body.get("author")
    location = body.get("location").capitalize()
    status = body.get("status")
    post = Post(
        image=image,
        message=message,
        author=author,
        location=location,
        status=status,
    )
    db.session.add(post)
    db.session.commit()
    return (
        jsonify({"message": "A post has been created", "post": post.id}),
        201,
    )


@posts.route("/post/like", methods=["POST"])
def like():
    body = request.get_json()
    for i in ["post_id", "user_id"]:
        if (
            not i in body.keys()
            or body[i] == ""
            or body[i] == None
            or not isinstance(body[i], int)
        ):
            return (
                jsonify({"message": f"{i} is needed"}),
                400,
            )
    post_id = body.get("post_id")
    user_id = body.get("user_id")
    post = Post.query.get(post_id)
    user = User.query.get(user_id)
    if post and user:
        if not user in post.likes:
            post.likes.append(user)
        else:
            post.likes.remove(user)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "A post has been liked",
                    "post": post.message,
                    "user": user.username,
                }
            ),
            201,
        )
    return (jsonify({"message": "post id and user id are needed"}), 404)


@posts.route("/posts", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    all_posts = list(map(lambda x: x.serialize(), posts))
    return jsonify(all_posts), 200
