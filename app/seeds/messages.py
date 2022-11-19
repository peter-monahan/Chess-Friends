from app.models import db, User, Friend_Request, Game_History, Game, Game_Request, Dm_View, Message


def seed_messages():

  user1 = User.query.filter(User.username == 'Demo').first()
  user2 = User.query.filter(User.username == 'hensell').first()
  james = User.query.filter(User.username == 'james').first()
  magnus = User.query.filter(User.username == 'magnus').first()

  dm1 = Message(sender_id=user1.id, receiver_id=user2.id, content='Hi im demo')
  dm2 = Message(sender_id=user2.id, receiver_id=user1.id, content='Hiiiiiii')
  dm3 = Message(sender_id=user2.id, receiver_id=user1.id, content='Hiiiiiiiiiiiiiiii')
  dm4 = Message(sender_id=user1.id, receiver_id=user2.id, content='Hii.')
  dm5 = Message(sender_id=user2.id, receiver_id=user1.id, content='Hiiiiiiiiiiiiiiiiiii')
  dm6 = Message(sender_id=user2.id, receiver_id=user1.id, content='Im Hensell')


  dm7 = Message(sender_id=james.id, receiver_id=magnus.id, content='yo bro')

  db.session.add(dm1)
  db.session.add(dm2)
  db.session.add(dm3)
  db.session.add(dm4)
  db.session.add(dm5)
  db.session.add(dm6)
  db.session.add(dm7)



  db.session.commit()
  q1 = Message.query.filter(Message.sender_id == user1.id, Message.receiver_id == user2.id)
  q2 = Message.query.filter(Message.sender_id == user2.id, Message.receiver_id == user1.id)

  messages = q1.union(q2).all()

  print(f'demo and hensell messages {[message.to_dict() for message in messages]}')

# Uses a raw SQL query to TRUNCATE the users table.
# SQLAlchemy doesn't have a built in function to do this
# TRUNCATE Removes all the data from the table, and RESET IDENTITY
# resets the auto incrementing primary key, CASCADE deletes any
# dependent entities
def undo_messages():
  db.session.execute('TRUNCATE messages RESTART IDENTITY CASCADE;')
  db.session.commit()
