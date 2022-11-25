from app.forms import GameRequestForm
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import User, Game, Game_Request, db
from datetime import datetime
from app.sockets import socketio
from app import chess_classes
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


@game_routes.route('/')
@login_required
def get_games():
    user = User.query.get(current_user.id)
    return {game.id: game.to_dict() for game in user.games}


@game_routes.route('/<int:id>', methods=["PUT"])
@login_required
def make_move(id):
    move = request.json
    game_record = Game.query.get(id)
    if game_record:
        game_data = json.load(game_record.json_data)
        if game_data['turn'] == 'white' and current_user.id == game_record.white_id:
            game = chess_classes.Game(game=game_data)
            success = game.move(move)
            if game.checkmate:
              pass
            elif game.stalemate:
              pass
            if success:
                game_record.json_data = json.dumps(game.to_dict())
                db.session.commit()
                if game_record.black_player.session_id:
                    socketio.emit('update_game', game.to_dict(),
                                  room=game_record.black_player.session_id)
                return game.to_dict()
        elif game_data['turn'] == 'black' and current_user.id == game_record.black_id:
            game = chess_classes.Game(game=game_data)
            success = game.move(move)
            if game.checkmate:
              pass
            elif game.stalemate:
              pass
            if success:
                game_record.json_data = json.dumps(game.to_dict())
                db.session.commit()
                if game_record.white_player.session_id:
                    socketio.emit('update_game', game.to_dict(),
                                  room=game_record.white_player.session_id)
                return game.to_dict()
        else:
            return {'errors': ['Unauthorized']}, 401
    else:
        return {'message': 'Game could not be found'}, 404


@game_routes.route('/<int:id>', methods=["DELETE"])
@login_required
def forfeit_game(id):
  return {'message': 'FORFEIT'}


@game_routes.route('/<int:id>/draw', methods=["PUT"])
@login_required
def offer_draw(id):
  return {'message': 'DRAW'}


@game_routes.route('/requests')
@login_required
def get_game_requests():
    user = User.query.get(current_user.id)

    res = {
        'sent': [game_request.to_dict() for game_request in user.sent_game_requests],
        'received': [game_request.to_dict() for game_request in user.received_game_requests]
    }
    return res


@game_routes.route('/requests', methods=['POST'])
@login_required
def create_game_request():
    form = GameRequestForm()
    if form.validate_on_submit:

        game_request = Game_Request(
            user_id=current_user.id, opponent_id=form.data['opponent_id'])
        db.session.add(game_request)
        db.session.commit()
        if form.data['opponent_id']:
            # ALERT MAY NEED TO BE INT WATCHOUT FOR BUGS
            receiver = User.query.get(form.data['opponent_id'])
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
            game_data = chess_classes.Game()
            game = Game(white_id=request.user_id, black_id=request.opponent_id,
                        json_data=json.dumps(game_data.to_dict()))
            db.session.delete(request)
            db.session.add(game)
            db.session.commit()
            if request.sender.session_id:
                socketio.emit('new_game', game.to_dict(),
                              room=request.sender.session_id)
            return game.to_dict()
        else:
            return {'errors': ['Unauthorized']}, 401
    else:
        return jsonify({'message': 'Game request could not be found'}), 404
