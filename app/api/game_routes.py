from app.forms import GameRequestForm
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import User, Game, Game_Request, db
from datetime import datetime
from app.sockets import socketio
from app import py_chess
import json

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


@game_routes.route('')
@login_required
def get_games():
    user = User.query.get(current_user.id)
    return {game.id: game.to_dict_with_opponent(current_user.id) for game in user.games}


@game_routes.route('/<int:id>')
@login_required
def get_game(id):
  game_record = Game.query.get(id)
  if game_record:
    if current_user.id == game_record.white_id or current_user.id == game_record.black_id:
      return game_record.to_dict_with_opponent(current_user.id)
    else:
      return {'errors': ['Unauthorized']}, 401
  else:
    return {'errors': ['Game could not be found']}, 404




@game_routes.route('/<int:id>', methods=["PUT"])
@login_required
def make_move(id):
    user = User.query.get(current_user.id)
    move = request.json
    game_record = Game.query.get(id)
    if game_record:
        game_data = json.loads(game_record.json_data)
        if game_data['turn'][0] == 'white' and current_user.id == game_record.white_id:

            game = py_chess.Game(game=game_data)
            success = game.move(move)
            if success:
                if game.checkmate or game.stalemate:
                    game_record.json_data = json.dumps(game.to_dict())

                    db.session.delete(game_record)
                    db.session.commit()
                else:
                    game_record.json_data = json.dumps(game.to_dict())
                    db.session.commit()

                if game_record.black_player.session_id:
                    socketio.emit('update_game', game_record.to_dict_with_opponent(game_record.black_id),
                                  room=game_record.black_player.session_id)
                socketio.emit('update_game', game_record.to_dict_with_opponent(current_user.id),
                                  room=user.session_id)
                return game_record.to_dict_with_opponent(current_user.id)
            else:
                return {'errors': ['Not a valid move']}, 400
        elif game_data['turn'][0] == 'black' and current_user.id == game_record.black_id:
            game = py_chess.Game(game=game_data)
            success = game.move(move)
            if success:
                if game.checkmate or game.stalemate:
                    game_record.json_data = json.dumps(game.to_dict())

                    db.session.delete(game_record)
                    db.session.commit()
                else:
                    game_record.json_data = json.dumps(game.to_dict())
                    db.session.commit()

                if game_record.white_player.session_id:
                    socketio.emit('update_game', game_record.to_dict_with_opponent(game_record.white_id),
                                  room=game_record.white_player.session_id)
                socketio.emit('update_game', game_record.to_dict_with_opponent(current_user.id),
                                  room=user.session_id)
                return game_record.to_dict_with_opponent(current_user.id)
            else:
                return {'errors': ['Not a valid move']}, 400
        else:
            return {'errors': ['Unauthorized']}, 401
    else:
        return {'errors': ['Game could not be found']}, 404


@game_routes.route('/<int:id>', methods=["DELETE"])
@login_required
def forfeit_game(id):
    game_record = Game.query.get(id)
    user = User.query.get(current_user.id)
    if game_record:
      game = py_chess.Game(game=json.loads(game_record.json_data))
      if current_user.id == game_record.white_id:
        game.forfeit_game('white')
        db.session.delete(game_record)
        db.session.commit()
        if game_record.black_player.session_id:
            socketio.emit('update_game', {**game_record.to_dict_with_opponent(game_record.black_id), 'data': game.to_dict()},
                          room=game_record.black_player.session_id)
        socketio.emit('update_game', {**game_record.to_dict_with_opponent(current_user.id), 'data': game.to_dict()},
                      room=user.session_id)
        return {**game_record.to_dict_with_opponent(current_user.id), 'data': game.to_dict()}
      elif current_user.id == game_record.black_id:
        game.forfeit_game('black')
        db.session.delete(game_record)
        db.session.commit()
        if game_record.white_player.session_id:
            socketio.emit('update_game', {**game_record.to_dict_with_opponent(game_record.white_id), 'data': game.to_dict()},
                          room=game_record.white_player.session_id)
        socketio.emit('update_game', {**game_record.to_dict_with_opponent(current_user.id), 'data': game.to_dict()},
                      room=user.session_id)
        return {**game_record.to_dict_with_opponent(current_user.id), 'data': game.to_dict()}
      else:
        return {'errors': ['Unauthorized']}, 401
    else:
      return {'errors': ['Game could not be found']}, 404


@game_routes.route('/<int:id>/draw', methods=["PUT"])
@login_required
def offer_draw(id):
  return {'message': 'DRAW'}


@game_routes.route('/requests')
@login_required
def get_game_requests():
    user = User.query.get(current_user.id)

    res = {
        'sent': {game_request.id: game_request.sent_to_dict() for game_request in user.sent_game_requests},
        'received': {game_request.id: game_request.received_to_dict() for game_request in user.received_game_requests}
    }
    return res


@game_routes.route('/requests', methods=['POST'])
@login_required
def create_game_request():
    form = GameRequestForm()
    if form.validate_on_submit:
        if current_user.id != form.data['opponent_id']:

            game_request = Game_Request(
                user_id=current_user.id, opponent_id=form.data['opponent_id'])
            db.session.add(game_request)
            db.session.commit()
            if form.data['opponent_id']:
                # ALERT MAY NEED TO BE INT WATCHOUT FOR BUGS
                receiver = User.query.get(form.data['opponent_id'])
                if receiver.session_id:
                    socketio.emit('new_game_request', {'gameRequest': game_request.received_to_dict(), 'requestType': 'received'},
                                  room=receiver.session_id)
            return game_request.sent_to_dict()
        else:
          return {'errors': ['Cannot create game request with self']}
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
                socketio.emit('delete_game_request', {
                              'request': request.to_dict(), 'requestType': 'sent'})
            return {'message': 'Success', 'item': request.to_dict(), 'requestType': 'received'}
        elif request.user_id == current_user.id:
            other_user = User.query.get(request.opponent_id)
            db.session.delete(request)
            db.session.commit()
            if other_user.session_id:
                socketio.emit('delete_game_request', {
                              'request': request.to_dict(), 'requestType': 'received'})
            return {'message': 'Success', 'item': request.to_dict(), 'requestType': 'sent'}
        else:
            return {'errors': ['Unauthorized']}, 401
    else:
        return jsonify({'message': 'Game request could not be found'}), 404


@game_routes.route('/requests/<int:id>', methods=["PUT"])
@login_required
def accept_game_request(id):
    request = Game_Request.query.get(id)

    if request:
        if request.opponent_id == current_user.id:
            game_data = py_chess.Game()
            game = Game(white_id=request.user_id, black_id=request.opponent_id,
                        json_data=json.dumps(game_data.to_dict()))
            db.session.delete(request)
            db.session.add(game)
            db.session.commit()
            if request.sender.session_id:
                socketio.emit('new_game', {'game': game.to_dict_with_opponent(request.sender.id), 'requestId':request.id},
                              room=request.sender.session_id)
            return game.to_dict_with_opponent(current_user.id)
        else:
            return {'errors': ['Unauthorized']}, 401
    else:
        return jsonify({'message': 'Game request could not be found'}), 404
