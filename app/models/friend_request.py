from .db import db
from datetime import datetime

class Friend_Request(db.Model):
  __tablename__ = 'friend_requests'
  id = db.Column(db.Integer, primary_key=True)
  sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now)
  updated_at = db.Column(db.DateTime, default=datetime.now)

  __table_args__ = (db.UniqueConstraint('sender_id', 'receiver_id', name='_sender_receiver_uc'),)

  sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_friend_requests', lazy='joined')
  receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_friend_requests', lazy='joined')


  def to_dict(self):
    return {
      'id': self.id,
      'sender_id': self.sender_id,
      'receiver_id': self.receiver_id,
      'created_at': self.created_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
      'updated_at': self.updated_at.strftime("%a, %d %b %Y %H:%M:%S %Z")
    }

  def sent_to_dict(self):
    return {
      'id': self.id,
      'sender_id': self.sender_id,
      'receiver_id': self.receiver_id,
      'created_at': self.created_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
      'updated_at': self.updated_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
      'receiver': self.receiver.to_dict()
    }

  def received_to_dict(self):
    return {
      'id': self.id,
      'sender_id': self.sender_id,
      'receiver_id': self.receiver_id,
      'created_at': self.created_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
      'updated_at': self.updated_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
      'sender': self.sender.to_dict()
    }
