from .db import db
from datetime import datetime

class Game_Request(db.Model):  # type: ignore
  __tablename__ = 'game_requests'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  opponent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  created_at = db.Column(db.DateTime, default=datetime.now)
  updated_at = db.Column(db.DateTime, default=datetime.now)

  sender = db.relationship('User', foreign_keys=[user_id], backref='sent_game_requests', lazy='raise')
  receiver = db.relationship('User', foreign_keys=[opponent_id], backref='received_game_requests', lazy='raise')


  def to_dict(self):
    return {
      'id': self.id,
      'user_id': self.user_id,
      'opponent_id': self.opponent_id,
      'created_at': self.created_at,
      'updated_at': self.updated_at
    }
