from app.models import db, User, Friend_Request, Game_History, Game, Game_Request, Dm_View, Message


def seed_game_requests():

  Demo = User.query.filter(User.username == 'Demo1').first()
  Demo2 = User.query.filter(User.username == 'Demo2').first()
  baylen = User.query.filter(User.username == 'baylen').first()
  zaviar = User.query.filter(User.username == 'zaviar').first()
  james = User.query.filter(User.username == 'james').first()
  magnus = User.query.filter(User.username == 'magnus').first()

  game1 = Game_Request(user_id=zaviar.id, opponent_id=Demo.id)
  game2 = Game_Request(user_id=magnus.id, opponent_id=baylen.id)
  game3 = Game_Request(user_id=james.id, opponent_id=magnus.id)
  game4 = Game_Request(user_id=Demo2.id, opponent_id=james.id)
  game5 = Game_Request(user_id=baylen.id, opponent_id=zaviar.id)
  game6 = Game_Request(user_id=Demo2.id, opponent_id=baylen.id)

  db.session.add(game1)
  db.session.add(game2)
  db.session.add(game3)
  db.session.add(game4)
  db.session.add(game5)
  db.session.add(game6)



  db.session.commit()


  print(f'zaviar\'s sent_game_requests {[game_request.to_dict() for game_request in zaviar.sent_game_requests]}')
  print(f'zaviar\'s received_game_requests {[game_request.to_dict() for game_request in zaviar.received_game_requests]}')

# Uses a raw SQL query to TRUNCATE the users table.
# SQLAlchemy doesn't have a built in function to do this
# TRUNCATE Removes all the data from the table, and RESET IDENTITY
# resets the auto incrementing primary key, CASCADE deletes any
# dependent entities
def undo_game_requests():
  db.session.execute('TRUNCATE game_requests RESTART IDENTITY CASCADE;')
  db.session.commit()
