from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import ValidationError
from app.models import User


def validate(form, field):
  # Checking if user exists
  receiver_id = field.data
  if receiver_id:
    user = User.query.get(receiver_id)
    if not user:
      raise ValidationError('User not found.')
  else:
    raise ValidationError('You must provide a receiver_id')


class FriendRequestForm(FlaskForm):
  receiver_id = IntegerField('receiver_id', validators=[validate])
