from app.models import db, User, Friend_Request, Game_History, Game, Game_Request, Dm_View, Message


def seed_friends():

  Demo = User.query.filter(User.username == 'Demo1').first()
  Demo2 = User.query.filter(User.username == 'Demo2').first()
  baylen = User.query.filter(User.username == 'baylen').first()
  zaviar = User.query.filter(User.username == 'zaviar').first()
  james = User.query.filter(User.username == 'james').first()
  blake = User.query.filter(User.username == 'blake').first()

  Demo2.befriend(Demo)
  Demo2.befriend(zaviar)
  Demo2.befriend(james)


  baylen.befriend(james)
  baylen.befriend(zaviar)
  baylen.befriend(blake)
  # print(f'Demo2\'s friends {[friend.to_dict() for friend in Demo2.friends]}')
  # print(f'blake\'s friends {[friend.to_dict() for friend in blake.friends]}')

  db.session.commit()

# Uses a raw SQL query to TRUNCATE the users table.
# SQLAlchemy doesn't have a built in function to do this
# TRUNCATE Removes all the data from the table, and RESET IDENTITY
# resets the auto incrementing primary key, CASCADE deletes any
# dependent entities
def undo_friends():
  db.session.execute('TRUNCATE friends RESTART IDENTITY CASCADE;')
  db.session.commit()
