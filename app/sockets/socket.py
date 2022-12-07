from flask_socketio import SocketIO, join_room, rooms, leave_room
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
    # print('==================connect', rooms())
    user = User.query.get(current_user.id)

    if user.session_id and rooms(user.session_id):
      join_room(user.session_id)
      join_room(request.sid, sid=user.session_id)
    else:
      user.session_id = request.sid
      user.updated_at = datetime.now()
      db.session.commit()



@socketio.on('disconnect')
def handle_disconnection():
  if current_user.is_authenticated:
    user = User.query.get(current_user.id)
    # print('==================disconnect', rooms())
    if len(rooms()) > 1:
      if user.session_id == request.sid:
        other_user = None
        for id in rooms():
          if id != request.sid:
            if not other_user:
              other_user = id
            join_room(other_user, sid=id)
            leave_room(user.session_id, sid=id)
        user.session_id = other_user
      else:
        leave_room(request.sid, sid=user.session_id)
    else:
      user.session_id = None
      user.updated_at = datetime.now()

    db.session.commit()
