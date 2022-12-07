from app.forms import FriendRequestForm
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import User, Friend_Request, db
from datetime import datetime
from app.sockets import socketio

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

@friend_routes.route('')
@login_required
def get_friends():
  user = User.query.get(current_user.id)
  return {friend.id: friend.to_dict() for friend in user.friends}


@friend_routes.route('/<int:id>', methods=["DELETE"])
@login_required
def delete_friendship(id):
  user = User.query.get(current_user.id)
  friend = User.query.get(id)

  if friend:
    if friend in user.friends:
      user.unfriend(friend)
      db.session.commit()
      if friend.session_id:
        socketio.emit('delete_friend', user.to_dict(),
                      room=friend.session_id)
      return {'message': 'Success', 'item': friend.to_dict()}
    else:
      return {'errors': ['User must be a friend to be unfriended']}, 400
  else:
    return jsonify({'message': 'User could not be found'}), 404



@friend_routes.route('/requests', methods=['POST'])
@login_required
def create_friend_request():
  form = FriendRequestForm()
  if form.validate_on_submit:
    if current_user.id != form.data['receiver_id']:
      receiver = User.query.get(form.data['receiver_id']) # ALERT MAY NEED TO BE INT WATCHOUT FOR BUGS
      friend_request = Friend_Request(sender_id=current_user.id, receiver_id=form.data['receiver_id'])
      db.session.add(friend_request)
      db.session.commit()
      if receiver.session_id:
        socketio.emit('new_friend_request', friend_request.to_dict(),
                    room=receiver.session_id)
      return friend_request.to_dict()
    else:
      return {'errors': ['Cannot send friend request to self']}
  else:
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@friend_routes.route('/requests')
@login_required
def get_friend_requests():
  user = User.query.get(current_user.id)
  res = {
    'sent': {friend_request.id: friend_request.sent_to_dict() for friend_request in user.sent_friend_requests},
    'received': {friend_request.id: friend_request.received_to_dict() for friend_request in user.received_friend_requests}
  }
  return res



@friend_routes.route('/requests/<int:id>', methods=["PUT"])
@login_required
def accept_friend_request(id):
  request = Friend_Request.query.get(id)

  if request:
    if request.receiver_id == current_user.id:
      request.receiver.befriend(request.sender)
      db.session.delete(request)
      db.session.commit()
      if request.sender.session_id:
        socketio.emit('new_friend', {'friend': request.receiver.to_dict(), 'requestId': request.id},
                      room=request.sender.session_id)
      return request.sender.to_dict()
    else:
      return {'errors': ['Unauthorized']}, 401
  else:
    return jsonify({'message': 'Friend request could not be found'}), 404



@friend_routes.route('/requests/<int:id>', methods=["DELETE"])
@login_required
def delete_friend_request(id):
  request = Friend_Request.query.get(id)

  if request:
    if request.receiver_id == current_user.id:
      other_user = User.query.get(request.sender_id)
      db.session.delete(request)
      db.session.commit()
      if other_user.session_id:
        socketio.emit('delete_friend_request', {'request': request.to_dict(), 'requestType': 'sent'})
      return {'message': 'Success', 'item': request.to_dict(), 'requestType': 'received'}
    elif request.sender_id == current_user.id:
      other_user = User.query.get(request.receiver_id)
      db.session.delete(request)
      db.session.commit()
      if other_user.session_id:
        socketio.emit('delete_friend_request', {'request': request.to_dict(), 'requestType': 'received'})
      return {'message': 'Success', 'item': request.to_dict(), 'requestType': 'sent'}
    else:
      return {'errors': ['Unauthorized']}, 401
  else:
    return jsonify({'message': 'Friend request could not be found'}), 404
