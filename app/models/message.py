from .db import db
from datetime import datetime


class Message(db.Model):  # type: ignore
  __tablename__ = 'messages'
  id = db.Column(db.Integer, primary_key=True)
  sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  content = db.Column(db.String(300), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
  updated_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

  sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages', lazy='raise')
  receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages', lazy='raise')

  def to_dict(self):
      return {
        'id': self.id,
        'sender_id': self.sender_id,
        'receiver_id': self.receiver_id,
        'content': self.content,
        'created_at': self.created_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
        'updated_at': self.updated_at.strftime("%a, %d %b %Y %H:%M:%S %Z")
      }
