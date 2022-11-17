from app.models import db, User, Friend_Request, Game_History, Game, Game_Request, Dm_View, Message


def seed_games():

  Demo = User.query.filter(User.username == 'Demo').first()
  hensell = User.query.filter(User.username == 'hensell').first()
  baylen = User.query.filter(User.username == 'baylen').first()
  zaviar = User.query.filter(User.username == 'zaviar').first()
  james = User.query.filter(User.username == 'james').first()
  magnus = User.query.filter(User.username == 'magnus').first()

  game1 = Game(white_id=Demo.id, black_id=magnus.id, json_data="{data}")
  game2 = Game(white_id=magnus.id, black_id=zaviar.id, json_data="{data}")
  game3 = Game(white_id=james.id, black_id=baylen.id, json_data="{data}")
  game4 = Game(white_id=hensell.id, black_id=magnus.id, json_data="{data}")
  game5 = Game(white_id=baylen.id, black_id=Demo.id, json_data="{data}")
  game6 = Game(white_id=hensell.id, black_id=Demo.id, json_data="{data}")

  db.session.add(game1)
  db.session.add(game2)
  db.session.add(game3)
  db.session.add(game4)
  db.session.add(game5)
  db.session.add(game6)



  db.session.commit()


  print(f'Demo\'s games {[game.to_dict() for game in Demo.games]}')
# Uses a raw SQL query to TRUNCATE the users table.
# SQLAlchemy doesn't have a built in function to do this
# TRUNCATE Removes all the data from the table, and RESET IDENTITY
# resets the auto incrementing primary key, CASCADE deletes any
# dependent entities
def undo_games():
  db.session.execute('TRUNCATE games RESTART IDENTITY CASCADE;')
  db.session.commit()
