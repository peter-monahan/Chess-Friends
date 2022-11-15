from app.models import db, User, Friend_Request, Game_History, Game, Game_Request, Dm_View, Message


def seed_friend_requests():

  req1 = Friend_Request(sender_id=1, receiver_id=3)
  req2 = Friend_Request(sender_id=3, receiver_id=2)

  db.session.add(req1)
  db.session.add(req2)

  db.session.commit()

# Uses a raw SQL query to TRUNCATE the users table.
# SQLAlchemy doesn't have a built in function to do this
# TRUNCATE Removes all the data from the table, and RESET IDENTITY
# resets the auto incrementing primary key, CASCADE deletes any
# dependent entities
def undo_friend_requests():
  db.session.execute('TRUNCATE friend_requests RESTART IDENTITY CASCADE;')
  db.session.commit()
