from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import ValidationError
from app.models import User


def user_exists(form, field):
  # Checking if user exists
  opponent_id = field.data
  if opponent_id and opponent_id > 0:
    user = User.query.get(opponent_id)
    if not user:
      raise ValidationError('User not found.')



class GameRequestForm(FlaskForm):
  opponent_id = IntegerField('opponent_id', validators=[user_exists])
