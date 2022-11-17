from .db import db
import datetime

class Game_History(db.Model):  # type: ignore
  __tablename__ = 'game_histories'
  id = db.Column(db.Integer, primary_key=True)
  game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
  white_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  black_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  json_data = db.Column(db.Text(), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
  updated_at = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)

  white_player = db.relationship('User', foreign_keys=[white_id], back_populates='game_histories', lazy='raise')
  black_player = db.relationship('User', foreign_keys=[black_id], back_populates='game_histories', lazy='raise')
  game = db.relationship('Game', back_populates='history', lazy='raise')

  def to_dict(self):
    return {
      'id': self.id,
      'game_id': self.game_id,
      'white_id': self.white_id,
      'black_id': self.black_id,
      'json_data': self.json_data,
      'created_at': self.created_at,
      'updated_at': self.updated_at
    }
