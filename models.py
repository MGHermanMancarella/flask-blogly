"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()  # create a SQLAlchemy instance
# create a function that ties your db object to your app object
# thus, allows your flask app to connect to the specified db

DEFAULT_IMAGE_URL = "https://picsum.photos/200"


def connect_db(app):
    """Connect to database."""
    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    first_name = db.Column(
        db.String(20),
        nullable=False,
        unique=False)

    last_name = db.Column(
        db.String(20),
        nullable=False,
        unique=False)

    image_url = db.Column(
        db.Text,
        default=DEFAULT_IMAGE_URL,
        unique=False)


class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    title = db.Column(
        db.String(30),
        nullable=False)

    content = db.Column(
        db.text,
        nullable=False)

    created_At = db.Column(
        db.DateTime,
        nullable=False)

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
    )
