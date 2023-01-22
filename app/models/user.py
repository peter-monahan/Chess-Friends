from .db import db
from .friend_request import Friend_Request
from .game_request import Game_Request
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
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow)

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
      'created_at': self.created_at.strftime("%a, %d %b %Y %H:%M:%S GMT"),
      'updated_at': self.updated_at.strftime("%a, %d %b %Y %H:%M:%S GMT"),
    }

  def to_dict_with_friend(self, session_id):
    user = User.query.get(session_id)
    sent_fr_req = Friend_Request.query.filter(Friend_Request.sender_id == session_id,
                              Friend_Request.receiver_id == self.id).first()
    received_fr_req = Friend_Request.query.filter(Friend_Request.sender_id == self.id,
                              Friend_Request.receiver_id == session_id).first()

    sent_gm_req = Game_Request.query.filter(Game_Request.user_id == session_id,
                              Game_Request.opponent_id == self.id).first()
    received_gm_req = Game_Request.query.filter(Game_Request.user_id == self.id,
                              Game_Request.opponent_id == session_id).first()
    if self in user.friends:
      is_friend = True
    else:
      is_friend = False

    if sent_fr_req:
      sent_fr_req = sent_fr_req.to_dict()
    if received_fr_req:
      received_fr_req = received_fr_req.to_dict()

    if sent_gm_req:
      sent_gm_req = sent_gm_req.to_dict()
    if received_gm_req:
      received_gm_req = received_gm_req.to_dict()

    return {
      'id': self.id,
      'username': self.username,
      'profile_image_url': self.profile_image_url,
      'bio': self.bio,
      'active': bool(self.session_id),
      'is_friend': is_friend,
      'created_at': self.created_at.strftime("%a, %d %b %Y %H:%M:%S GMT"),
      'updated_at': self.updated_at.strftime("%a, %d %b %Y %H:%M:%S GMT"),
      'sent_to_friend_req': sent_fr_req,
      'received_from_friend_req': received_fr_req,
      'sent_to_game_req': sent_gm_req,
      'received_from_game_req': received_gm_req,
    }

  def to_dict_little(self):
    # May add is_friend bool at a later date
    return {
      'id': self.id,
      'username': self.username,
      'profile_image_url': self.profile_image_url,
      'active': bool(self.session_id),
      'updated_at': self.updated_at.strftime("%a, %d %b %Y %H:%M:%S GMT"),
    }

  def to_dict_private(self):
    return {
      'id': self.id,
      'username': self.username,
      'email': self.email,
      'profile_image_url': self.profile_image_url,
      'bio': self.bio,
      'active': bool(self.session_id),
      'created_at': self.created_at.strftime("%a, %d %b %Y %H:%M:%S GMT"),
      'updated_at': self.updated_at.strftime("%a, %d %b %Y %H:%M:%S GMT"),
    }
