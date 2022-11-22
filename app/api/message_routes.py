from app.forms import MessageForm
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import User, Dm_View, Message, db
from datetime import datetime
from app.sockets import socketio
# from flask_socketio import emit

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


@message_routes.route('/views/with/<int:id>', methods=["POST"])
@login_required
def create_dm_view(id):
    user = User.query.get(current_user.id)
    other_user = User.query.get(id)

    dm1exists = Dm_View.query.filter(
        Dm_View.user_id == user.id, Dm_View.other_user_id == other_user.id).first()
    dm2exists = Dm_View.query.filter(
        Dm_View.user_id == other_user.id, Dm_View.other_user_id == user.id).first()

    if not dm1exists:
        dm1 = Dm_View(user_id=user.id, other_user_id=other_user.id)
        db.session.add(dm1)
        if not dm2exists:
            dm2 = Dm_View(user_id=other_user.id, other_user_id=user.id)
            db.session.add(dm2)
            db.session.commit()
            if other_user.session_id:
                socketio.emit('new_chat', dm2.to_dict(),
                              room=other_user.session_id)
        else:
            db.session.commit()
        return dm1.to_dict()
    else:
        return {'errors': ['Chat already exists']}, 400

    # views = Dm_View.query.filter(Dm_View.user_id == current_user.id).all()

    # TODO: add emit to other user if they are online


@message_routes.route('/views/<int:id>', methods=["DELETE"])
@login_required
def delete_dm_view(id):
    view = Dm_View.query.get(id)
    if view.user_id == current_user.id:
        db.session.delete(view)
        db.session.commit()
        return {"message": "Success"}
    else:
        return {'errors': ['Unauthorized']}, 401


@message_routes.route('/with/<int:id>')
@login_required
def get_conversation(id):
    q1 = Message.query.filter(Message.sender_id == current_user.id,
                              Message.receiver_id == id)
    q2 = Message.query.filter(Message.sender_id == id,
                              Message.receiver_id == current_user.id)

    messages = q1.union(q2).all()

    return {message.id: message.to_dict() for message in messages}


@message_routes.route('/with/<int:id>', methods=["POST"])
@login_required
def add_to_conversation(id):
    form = MessageForm()
    if form.validate_on_submit:
        other_user = User.query.get(id)
        message = Message(sender_id=current_user.id,
                          receiver_id=id, content=form.data['content'])
        db.session.add(message)
        db.session.commit()
        if other_user.session_id:
                socketio.emit('new_message', message.to_dict(),
                              room=other_user.session_id)
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
            other_user = User.query.get(message.receiver_id)
            message.content = form.data['content']
            message.updated_at = datetime.now()
            db.session.commit()
            if other_user.session_id:
                socketio.emit('edit_message', message.to_dict(),
                              room=other_user.session_id)
            return message.to_dict()
        else:
            return {'errors': validation_errors_to_error_messages(form.errors)}, 401
    else:
        return {'errors': ['Unauthorized']}, 401


@message_routes.route('/<int:id>', methods=["DELETE"])
@login_required
def delete_message(id):
    message = Message.query.get(id)
    if message.sender_id == current_user.id:
        other_user = User.query.get(message.receiver_id)
        db.session.delete(message)
        db.session.commit()
        if other_user.session_id:
            socketio.emit('delete_message', message.to_dict(),
                          room=other_user.session_id)
        return {"message": "Successfully deleted message", "item": message.to_dict()}, 200
    else:
        return {'errors': ['Unauthorized']}, 401
