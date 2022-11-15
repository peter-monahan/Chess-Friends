from .db import db
from datetime import datetime

class Game(db.Model):  # type: ignore
  __tablename__ = 'games'
  id = db.Column(db.Integer, primary_key=True)
  white_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  black_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  json_data = db.Column(db.Text(), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
  updated_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

  white_player = db.relationship('User', foreign_keys=[white_id], back_populates='games', lazy='raise')
  black_player = db.relationship('User', foreign_keys=[black_id], back_populates='games', lazy='raise')
  history = db.relationship('Game_History', back_populates='game', lazy='raise')
