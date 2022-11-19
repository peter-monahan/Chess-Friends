from app.models import db, User, Friend_Request, Game_History, Game, Game_Request, Dm_View, Message

# Adds a demo user, you can add other users here if you want
def seed_users():
  demo = User(
      username='Demo', email='demo@aa.io', password='password')
  user2 = User(
      username='hensell', email='hensell@aa.io', password='password')
  user3 = User(
      username='baylen', email='baylen@aa.io', password='password')
  user4 = User(
      username='zaviar', email='zaviar@aa.io', password='password')
  user5 = User(
      username='james', email='james@aa.io', password='password')
  user6 = User(
      username='magnus', email='magnus@aa.io', password='password')


  db.session.add(demo)
  db.session.add(user2)
  db.session.add(user3)
  db.session.add(user4)
  db.session.add(user5)
  db.session.add(user6)

  db.session.commit()
  print([demo.to_dict(), user2.to_dict(), user3.to_dict(), user4.to_dict(), user5.to_dict(), user6.to_dict(), ])

# Uses a raw SQL query to TRUNCATE the users table.
# SQLAlchemy doesn't have a built in function to do this
# TRUNCATE Removes all the data from the table, and RESET IDENTITY
# resets the auto incrementing primary key, CASCADE deletes any
# dependent entities
def undo_users():
  db.session.execute('TRUNCATE users RESTART IDENTITY CASCADE;')
  db.session.commit()
