from flask_socketio import SocketIO
import os
from flask import request
from flask_login import current_user
from app.models import User, db
from datetime import datetime

if os.environ.get("FLASK_ENV") == "production":
    origins = [
        "http://justchess.herokuapp.com",
        "https://justchess.herokuapp.com"
    ]
else:
    origins = "*"

# create your SocketIO instance
socketio = SocketIO(cors_allowed_origins=origins)

@socketio.on('connect')
def handle_connection():
  if current_user.is_authenticated:
    user = User.query.get(current_user.id)
    user.session_id = request.sid
    user.updated_at = datetime.now()
    db.session.commit()


@socketio.on('disconnect')
def handle_disconnection():
  if current_user.is_authenticated:
    user = User.query.get(current_user.id)
    user.session_id = None
    user.updated_at = datetime.now()
    db.session.commit()
