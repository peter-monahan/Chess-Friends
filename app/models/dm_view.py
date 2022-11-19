from .db import db
from datetime import datetime


class Dm_View(db.Model):  # type: ignore
  __tablename__ = 'dm_views'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  other_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
  updated_at = db.Column(db.DateTime, default=datetime.now, nullable=False)


  # messages = db.relationship("Message", primaryjoin="or_(Dm_View.user_id==Message.sender_id and Dm_View.other_user_id==Message.receiver_id, " "Dm_View.other_user_id==Message.sender_id and Dm_View.user_id==Message.receiver_id)", lazy='raise')
  # will have to be done as a query when needed ^^^
  def to_dict(self):
    return {
      'id': self.id,
      'user_id': self.user_id,
      'other_user_id': self.other_user_id,
      'created_at': self.created_at,
      'updated_at': self.updated_at
    }
