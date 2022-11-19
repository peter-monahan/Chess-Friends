from app.models import db, User, Friend_Request, Game_History, Game, Game_Request, Dm_View, Message


def seed_friends():

  Demo = User.query.filter(User.username == 'Demo').first()
  hensell = User.query.filter(User.username == 'hensell').first()
  baylen = User.query.filter(User.username == 'baylen').first()
  zaviar = User.query.filter(User.username == 'zaviar').first()
  james = User.query.filter(User.username == 'james').first()
  magnus = User.query.filter(User.username == 'magnus').first()

  hensell.befriend(baylen)
  hensell.befriend(Demo)
  hensell.befriend(zaviar)
  hensell.befriend(james)


  baylen.befriend(james)
  baylen.befriend(zaviar)

  print(f'hensell\'s friends {[friend.to_dict() for friend in hensell.friends]}')
  print(f'magnus\' friends {[friend.to_dict() for friend in magnus.friends]}')

  db.session.commit()

# Uses a raw SQL query to TRUNCATE the users table.
# SQLAlchemy doesn't have a built in function to do this
# TRUNCATE Removes all the data from the table, and RESET IDENTITY
# resets the auto incrementing primary key, CASCADE deletes any
# dependent entities
def undo_friends():
  db.session.execute('TRUNCATE friends RESTART IDENTITY CASCADE;')
  db.session.commit()
