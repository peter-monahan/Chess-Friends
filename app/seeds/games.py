from app.models import db, User, Game
from app import py_chess
import json


def seed_games():

    Demo = User.query.filter(User.username == 'Demo1').first()
    Demo2 = User.query.filter(User.username == 'Demo2').first()
    baylen = User.query.filter(User.username == 'baylen').first()
    zaviar = User.query.filter(User.username == 'zaviar').first()
    james = User.query.filter(User.username == 'james').first()
    blake = User.query.filter(User.username == 'blake').first()

    game_data1 = py_chess.Game()



    game1 = Game(white_id=Demo.id, black_id=blake.id,
                 json_data=json.dumps(game_data1.to_dict()))
    game2 = Game(white_id=blake.id, black_id=zaviar.id,
                 json_data=json.dumps(game_data1.to_dict()))
    game3 = Game(white_id=james.id, black_id=baylen.id,
                 json_data=json.dumps(game_data1.to_dict()))
    game4 = Game(white_id=Demo2.id, black_id=blake.id,
                 json_data=json.dumps(game_data1.to_dict()))
    game5 = Game(white_id=baylen.id, black_id=Demo.id,
                 json_data=json.dumps(game_data1.to_dict()))
    game6 = Game(white_id=Demo2.id, black_id=Demo.id,
                 json_data=json.dumps(game_data1.to_dict()))

    db.session.add(game1)
    db.session.add(game2)
    db.session.add(game3)
    db.session.add(game4)
    db.session.add(game5)
    db.session.add(game6)

    db.session.commit()
# Uses a raw SQL query to TRUNCATE the users table.
# SQLAlchemy doesn't have a built in function to do this
# TRUNCATE Removes all the data from the table, and RESET IDENTITY
# resets the auto incrementing primary key, CASCADE deletes any
# dependent entities


def undo_games():
    db.session.execute('TRUNCATE games RESTART IDENTITY CASCADE;')
    db.session.commit()
