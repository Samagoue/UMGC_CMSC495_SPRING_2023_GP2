from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from giftpal import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    dob = db.Column(db.String(8), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    events = db.relationship("UserEvent", back_populates="user")
    # groups = db.relationship("UserGroup", back_populates="user")
    wishlists = db.relationship("Wishlist", back_populates="user")
    given_pairs = db.relationship("Pair", back_populates="giver", foreign_keys="Pair.giver_id")
    received_pairs = db.relationship("Pair", back_populates="receiver", foreign_keys="Pair.receiver_id")

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(8), nullable=False)
    type = db.Column(db.String(50))

    users = db.relationship("UserEvent", back_populates="event")

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    wish = db.Column(db.Text, nullable=False)

    user = db.relationship("User", back_populates="wishlists")

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100), nullable=False)
    min_dollar_amount = db.Column(db.Integer, nullable=False)
    # group_email = db.Column(db.String(50), unique=True, nullable=False)
    # group_password = db.Column(db.String(64), nullable=False)
    pairs = db.relationship("Pair", back_populates="group")
    # users = db.relationship("UserGroup", back_populates="group")

class Pair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    giver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

    giver = db.relationship("User", back_populates="given_pairs", foreign_keys=[giver_id])
    receiver = db.relationship("User", back_populates="received_pairs", foreign_keys=[receiver_id])
    group = db.relationship("Group", back_populates="pairs")

class UserEvent(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)
    user = db.relationship("User", back_populates="events")
    event = db.relationship("Event", back_populates="users")

class UserGroup(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    # user = db.relationship("User", back_populates="groups")
    # group = db.relationship("Group", back_populates="users")
    is_admin = db.Column(db.Boolean, default=False)
