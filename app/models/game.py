from .db import db
from datetime import datetime
from app import py_chess
import json

class Game(db.Model):
  __tablename__ = 'games'
  id = db.Column(db.Integer, primary_key=True)
  white_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  black_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  bot_id = db.Column(db.Integer)
  json_data = db.Column(db.Text(), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
  updated_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

  white_player = db.relationship('User', foreign_keys=[white_id], back_populates='games', lazy='joined')
  black_player = db.relationship('User', foreign_keys=[black_id], back_populates='games', lazy='joined')
  history = db.relationship('Game_History', back_populates='game', lazy='raise')

  def to_dict(self):
    return {
      'id': self.id,
      'white_id': self.white_id,
      'black_id': self.black_id,
      'data': json.loads(self.json_data),
      'created_at': self.created_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
      'updated_at': self.updated_at.strftime("%a, %d %b %Y %H:%M:%S %Z")
    }

  def to_dict_with_opponent(self, user_id):
    if self.black_id == None:
      created_at = self.created_at
      updated_at = self.updated_at
      if created_at or updated_at:
        created_at = self.created_at.strftime("%a, %d %b %Y %H:%M:%S %Z")
        updated_at = self.updated_at.strftime("%a, %d %b %Y %H:%M:%S %Z")
      return {
        'id': self.id,
        'white_id': self.white_id,
        'black_id': self.black_id,
        'data': json.loads(self.json_data),
        'created_at': created_at,
        'updated_at': updated_at,
        'opponent': py_chess.bots_profiles[(-self.bot_id)-1].to_dict()
      }
    elif self.white_id == None:
      created_at = self.created_at
      updated_at = self.updated_at
      if created_at or updated_at:
        created_at = self.created_at.strftime("%a, %d %b %Y %H:%M:%S %Z")
        updated_at = self.updated_at.strftime("%a, %d %b %Y %H:%M:%S %Z")
      return {
        'id': self.id,
        'white_id': self.white_id,
        'black_id': self.black_id,
        'data': json.loads(self.json_data),
        'created_at': created_at,
        'updated_at': updated_at,
        'opponent': py_chess.bots_profiles[(-self.bot_id)-1].to_dict()
      }
    elif user_id == self.white_id:
      return {
        'id': self.id,
        'white_id': self.white_id,
        'black_id': self.black_id,
        'data': json.loads(self.json_data),
        'created_at': self.created_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
        'updated_at': self.updated_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
        'opponent': self.black_player.to_dict()
      }
    else:
      return {
        'id': self.id,
        'white_id': self.white_id,
        'black_id': self.black_id,
        'data': json.loads(self.json_data),
        'created_at': self.created_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
        'updated_at': self.updated_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
        'opponent': self.white_player.to_dict()
      }
