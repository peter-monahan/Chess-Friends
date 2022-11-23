from app.forms import GameRequestForm
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import User, Game, Game_Request, db
from datetime import datetime
from app.sockets import socketio
from app.chess_classes import Game

game_routes = Blueprint('games', __name__)


def validation_errors_to_error_messages(validation_errors):
    """
    Simple function that turns the WTForms validation errors into a simple list
    """
    errorMessages = []
    for field in validation_errors:
        for error in validation_errors[field]:
            errorMessages.append(f'{field} : {error}')
    return errorMessages

@game_routes.route('/')
@login_required
def get_games():
  user = User.query.get(current_user.id)
  return {game.id: game.to_dict() for game in user.games}



@game_routes.route('/requests')
@login_required
def get_game_requests():
  user = User.query.get(current_user.id)
  game = Game()
  print(game.to_dict())
  return game.to_dict()
  # res = {
  #   'sent': [game_request.to_dict() for game_request in user.sent_game_requests],
  #   'received': [game_request.to_dict() for game_request in user.received_game_requests]
  # }
  # return res


@game_routes.route('/requests', methods=['POST'])
@login_required
def create_game_request():
  form = GameRequestForm()
  if form.validate_on_submit:

    game_request = Game_Request(user_id=current_user.id, opponent_id=form.data['opponent_id'])
    db.session.add(game_request)
    db.session.commit()
    if form.data['opponent_id']:
      receiver = User.query.get(form.data['opponent_id']) # ALERT MAY NEED TO BE INT WATCHOUT FOR BUGS
      if receiver.session_id:
        socketio.emit('new_game_request', game_request.to_dict(),
                    room=receiver.session_id)
    return game_request.to_dict()
  else:
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401


@game_routes.route('/requests/<int:id>', methods=["DELETE"])
@login_required
def delete_game_request(id):
  request = Game_Request.query.get(id)

  if request:
    if request.opponent_id == current_user.id:
      other_user = User.query.get(request.user_id)
      db.session.delete(request)
      db.session.commit()
      if other_user.session_id:
        socketio.emit('delete_game_request', {'request': request.to_dict(), 'requestType': 'sent'})
      return {'message': 'Success', 'item': request.to_dict(), 'requestType': 'received'}
    elif request.user_id == current_user.id:
      other_user = User.query.get(request.opponent_id)
      db.session.delete(request)
      db.session.commit()
      if other_user.session_id:
        socketio.emit('delete_game_request', {'request': request.to_dict(), 'requestType': 'received'})
      return {'message': 'Success', 'item': request.to_dict(), 'requestType': 'sent'}
    else:
      return {'errors': ['Unauthorized']}, 401
  else:
    return jsonify({'message': 'Game request could not be found'}), 404
