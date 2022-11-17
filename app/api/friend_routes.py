from app.forms import FriendRequestForm
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import User, Friend_Request, db
from datetime import datetime

friend_routes = Blueprint('friends', __name__)




def validation_errors_to_error_messages(validation_errors):
    """
    Simple function that turns the WTForms validation errors into a simple list
    """
    errorMessages = []
    for field in validation_errors:
        for error in validation_errors[field]:
            errorMessages.append(f'{field} : {error}')
    return errorMessages



@friend_routes.route('/<int:id>', methods=["DELETE"])
@login_required
def delete_friendship(id):
  user = User.query.get(current_user.id)
  friend = User.query.get(id)

  if friend:
    if friend in user.friends:
      user.unfriend(friend)
      db.session.commit()
      return {'message': 'Success'}
    else:
      return {'errors': ['User must be a friend to be unfriended']}
  else:
    return jsonify({'message': 'User could not be found'}), 404



@friend_routes.route('/requests', methods=['POST'])
@login_required
def create_friend_request():
  form = FriendRequestForm()
  if form.validate_on_submit:
    friend_request = Friend_Request(sender_id=current_user.id, receiver_id=form.data['receiver_id'])
    db.session.add(friend_request)
    db.session.commit()

    return friend_request.to_dict()
  else:
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@friend_routes.route('/requests')
@login_required
def get_friend_requests():
  user = User.query.get(current_user.id)
  res = {
    'sent_friend_requests': [friend_request.to_dict() for friend_request in user.sent_friend_requests],
    'received_friend_requests': [friend_request.to_dict() for friend_request in user.received_friend_requests]
  }
  return res



@friend_routes.route('/requests/<int:id>', methods=["PUT"])
@login_required
def accept_friend_request(id):
  request = Friend_Request.query.get(id)

  if request:
    if request.receiver_id == current_user.id:
      # user = User.query.get(current_user.id)
      # friend = User.query.get(request.sender_id)
      # user.befriend(friend)
      request.receiver.befriend(request.sender)
      db.session.delete(request)
      db.session.commit()
      return {'message': 'Success'}
    else:
      return {'errors': ['Unauthorized']}
  else:
    return jsonify({'message': 'Friend request could not be found'}), 404



@friend_routes.route('/requests/<int:id>', methods=["DELETE"])
@login_required
def delete_friend_request(id):
  request = Friend_Request.query.get(id)

  if request:
    if request.receiver_id == current_user.id or request.sender_id == current_user.id:
      db.session.delete(request)
      db.session.commit()
      return {'message': 'Success'}
    else:
      return {'errors': ['Unauthorized']}
  else:
    return jsonify({'message': 'Friend request could not be found'}), 404
