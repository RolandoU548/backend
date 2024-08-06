from utils.db import db
from datetime import datetime


post_like_association = db.Table(
    "post_like_association",
    db.Column("user", db.Integer, db.ForeignKey("user.id")),
    db.Column("post", db.Integer, db.ForeignKey("post.id")),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(300), nullable=True)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(10), unique=False, nullable=False)

    def init(self, avatar, name, surname, username, password):
        self.avatar = avatar
        self.name = name
        self.surname = surname
        self.username = username
        self.password = password

    def repr(self):
        return "<User %r>" % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "avatar": self.avatar,
            "surname": self.surname,
            "username": self.username,
        }


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(300), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    likes = db.relationship("User", secondary=post_like_association)
    author = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    location = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(10), nullable=False)

    def init(self, image, message, author, location, status):
        self.image = image
        self.message = message
        self.author = author
        self.location = location
        self.status = status

    def repr(self):
        return "<Post %r>" % self.message

    def serialize(self):
        return {
            "id": self.id,
            "image": self.image,
            "message": self.message.capitalize(),
            "likes": [user.serialize() for user in self.likes],
            "author": self.author,
            "author_name": User.query.get(self.author).username,
            "created_at": self.created_at,
            "location": self.location.capitalize(),
            "status": self.status,
        }
