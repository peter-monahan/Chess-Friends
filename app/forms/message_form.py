from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import ValidationError


def validate(form, field):
  content = field.data
  if content:
    if (len(content) == 0 or len(content.split()) == len(content)+1):
      raise ValidationError('You must provide at least one character')
  else:
    raise ValidationError('You must provide content')


class MessageForm(FlaskForm):
  content = StringField('content', validators=[validate])
