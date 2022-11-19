from app.forms import GameRequestForm
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import User, Game, Game_Request, db
from datetime import datetime

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


@game_routes.route('/requests', methods=['POST'])
@login_required
def create_game_request():
  curr_user_id = current_user.id
  form = GameRequestForm()
  if form.validate_on_submit:
    game_request = Game_Request(user_id=curr_user_id, opponent_id=form.data['opponent_id'])
    db.session.add(game_request)
    db.session.commit()

    return game_request.to_dict()
