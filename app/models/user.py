from .db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

friendship = db.Table(
  "friendships",
  db.Column("user_id", db.Integer, db.ForeignKey('users.id'), index=True),
  db.Column("friend_id", db.Integer, db.ForeignKey('users.id'))
)

class User(db.Model, UserMixin):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(40), nullable=False, unique=True)
  email = db.Column(db.String(255), nullable=False, unique=True)
  hashed_password = db.Column(db.String(255), nullable=False)
  profile_image_url = db.Column(db.String(300))
  bio = db.Column(db.String(300))
  session_id = db.Column(db.Text())
  created_at = db.Column(db.DateTime, default=datetime.now)
  updated_at = db.Column(db.DateTime, default=datetime.now)

  friends = db.relationship(
    "User",
    secondary=friendship,
    primaryjoin=(friendship.c.user_id == id),
    secondaryjoin=(friendship.c.friend_id == id)
  )

  games = db.relationship("Game", primaryjoin="or_(User.id==Game.white_id, " "User.id==Game.black_id)")
  game_histories = db.relationship("Game_History", primaryjoin="or_(User.id==Game_History.white_id, " "User.id==Game_History.black_id)")


  def befriend(self, friend):
    if friend not in self.friends:
      self.friends.append(friend)
      friend.friends.append(self)

  def unfriend(self, friend):
    if friend in self.friends:
      self.friends.remove(friend)
      friend.friends.remove(self)


  @property
  def password(self):
    return self.hashed_password

  @password.setter
  def password(self, password):
    self.hashed_password = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password, password)

  def to_dict(self):
    return {
      'id': self.id,
      'username': self.username,
      'profile_image_url': self.profile_image_url,
      'bio': self.bio,
      'active': bool(self.session_id),
      'created_at': self.created_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
      'updated_at': self.updated_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
    }

  def to_dict_little(self):
    # May add is_friend bool at a later date
    return {
      'id': self.id,
      'username': self.username,
      'profile_image_url': self.profile_image_url,
      'active': bool(self.session_id),
      'updated_at': self.updated_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
    }

  def to_dict_private(self):
    return {
      'id': self.id,
      'username': self.username,
      'email': self.email,
      'profile_image_url': self.profile_image_url,
      'bio': self.bio,
      'active': bool(self.session_id),
      'created_at': self.created_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
      'updated_at': self.updated_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
    }
