from app.models import db, User, Friend_Request, Game_History, Game, Game_Request, Dm_View, Message


def seed_messages():

  user1 = User.query.filter(User.username == 'Demo1').first()
  user2 = User.query.filter(User.username == 'Demo2').first()

  dm1 = Message(sender_id=user1.id, receiver_id=user2.id, content='Hi im demo1!')
  dm2 = Message(sender_id=user2.id, receiver_id=user1.id, content='Hey what\'s up?')
  dm3 = Message(sender_id=user2.id, receiver_id=user1.id, content='You wanna play chess??')
  dm4 = Message(sender_id=user1.id, receiver_id=user2.id, content='Sure')
  dm5 = Message(sender_id=user2.id, receiver_id=user1.id, content='Sweet! just sent you an invite')
  dm6 = Message(sender_id=user2.id, receiver_id=user1.id, content='Got it')



  db.session.add(dm1)
  db.session.add(dm2)
  db.session.add(dm3)
  db.session.add(dm4)
  db.session.add(dm5)
  db.session.add(dm6)
  # db.session.add(dm7)



  db.session.commit()
  # q1 = Message.query.filter(Message.sender_id == user1.id, Message.receiver_id == user2.id)
  # q2 = Message.query.filter(Message.sender_id == user2.id, Message.receiver_id == user1.id)

  # messages = q1.union(q2).all()

  # print(f'demo1 and demo2 messages {[message.to_dict() for message in messages]}')

# Uses a raw SQL query to TRUNCATE the users table.
# SQLAlchemy doesn't have a built in function to do this
# TRUNCATE Removes all the data from the table, and RESET IDENTITY
# resets the auto incrementing primary key, CASCADE deletes any
# dependent entities
def undo_messages():
  db.session.execute('TRUNCATE messages RESTART IDENTITY CASCADE;')
  db.session.commit()
