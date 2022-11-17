from app.forms import MessageForm
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import User, Dm_View, Message, db
from datetime import datetime

message_routes = Blueprint('messages', __name__)




def validation_errors_to_error_messages(validation_errors):
    """
    Simple function that turns the WTForms validation errors into a simple list
    """
    errorMessages = []
    for field in validation_errors:
        for error in validation_errors[field]:
            errorMessages.append(f'{field} : {error}')
    return errorMessages



@message_routes.route('/views')
@login_required
def get_dm_views():
  views = Dm_View.query.filter(Dm_View.user_id == current_user.id).all()

  return {view.id: view.to_dict() for view in views}

@message_routes.route('/with/<int:id>')
@login_required
def get_conversation(id):
  q1 = Message.query.filter(Message.sender_id == 1, Message.receiver_id == id)
  q2 = Message.query.filter(Message.sender_id == id, Message.receiver_id == 1)

  messages = q1.union(q2).all()

  return {message.id: message.to_dict() for message in messages}

@message_routes.route('/with/<int:id>', methods=["POST"])
@login_required
def add_to_conversation(id):
  form = MessageForm()
  if form.validate_on_submit:
    message = Message(sender_id=current_user.id, receiver_id=id, content=form.data['content'])
    db.session.add(message)
    db.session.commit()
    return message.to_dict()
  else:
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401

@message_routes.route('/<int:id>', methods=["PUT"])
@login_required
def edit_message(id):
  message = Message.query.get(id)
  form = MessageForm()
  if message.sender_id == current_user.id:
    if form.validate_on_submit:
      message.content = form.data['content']
      message.updated_at = datetime.now()
      db.session.commit()
      return message.to_dict()
    else:
      return {'errors': validation_errors_to_error_messages(form.errors)}, 401
  else:
    return {'errors': ['Unauthorized']}

@message_routes.route('/<int:id>', methods=["DELETE"])
@login_required
def delete_message(id):
  message = Message.query.get(id)
  if message.sender_id == current_user.id:
    db.session.delete(message)
    db.session.commit()
    return {"message": "Successfully deleted comment"}, 200
  else:
    return {'errors': ['Unauthorized']}
