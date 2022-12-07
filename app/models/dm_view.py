from .db import db
from .message import Message
from datetime import datetime


class Dm_View(db.Model):  # type: ignore
  __tablename__ = 'dm_views'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  other_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
  updated_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

  __table_args__ = (db.UniqueConstraint('user_id', 'other_user_id', name='_user_other_uc'),)

  user = db.relationship('User', foreign_keys=[other_user_id], lazy='joined')

  # messages = db.relationship("Message", primaryjoin="or_(Dm_View.user_id==Message.sender_id and Dm_View.other_user_id==Message.receiver_id, " "Dm_View.other_user_id==Message.sender_id and Dm_View.user_id==Message.receiver_id)", lazy='raise')
  # will have to be done as a query when needed ^^^
  def to_dict(self):
    q1 = Message.query.filter(Message.sender_id ==self.user_id,
                              Message.receiver_id == self.other_user_id).order_by(Message.id.desc()).first()
    q2 = Message.query.filter(Message.sender_id == self.other_user_id,
                              Message.receiver_id ==self.user_id).order_by(Message.id.desc()).first()
    # message = q1.union(q2).first()
    if not q2 or q1 and q1.id > q2.id:
      message = q1
    else:
      message = q2

    if message:
      message = message.to_dict()

    return {
      'id': self.id,
      'user_id': self.user_id,
      'other_user_id': self.other_user_id,
      'created_at': self.created_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
      'updated_at': self.updated_at.strftime("%a, %d %b %Y %H:%M:%S %Z"),
      'user': self.user.to_dict(),
      'message': message
    }
