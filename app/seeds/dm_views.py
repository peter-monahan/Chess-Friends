from app.models import db, User, Friend_Request, Game_History, Game, Game_Request, Dm_View, Message


def seed_dms():

  user1 = User.query.filter(User.username == 'Demo1').first()
  user2 = User.query.filter(User.username == 'Demo2').first()
  james = User.query.filter(User.username == 'james').first()
  magnus = User.query.filter(User.username == 'magnus').first()

  dm1 = Dm_View(user_id=user1.id, other_user_id=user2.id)
  dm2 = Dm_View(user_id=user2.id, other_user_id=user1.id)
  dm3 = Dm_View(user_id=james.id, other_user_id=magnus.id)

  db.session.add(dm1)
  db.session.add(dm2)
  db.session.add(dm3)



  db.session.commit()


# Uses a raw SQL query to TRUNCATE the users table.
# SQLAlchemy doesn't have a built in function to do this
# TRUNCATE Removes all the data from the table, and RESET IDENTITY
# resets the auto incrementing primary key, CASCADE deletes any
# dependent entities
def undo_dms():
  db.session.execute('TRUNCATE dm_view RESTART IDENTITY CASCADE;')
  db.session.commit()
