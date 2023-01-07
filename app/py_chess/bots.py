from .Game import Game
import random
def rando_man(game):
  keys = list(game.valid_moves.keys())
  choiceKey = random.choice(keys)
  chosen_coords = random.choice(game.valid_moves[choiceKey])

  return { 'move': [[int(num) for num in choiceKey.split(',')], chosen_coords]}

bots = [
  rando_man,
]

class Bot_Profile:
  def __init__(self, id, bio, username):
    self.id = id
    self.bio = bio
    self.username = username

  active = True
  profile_image_url = None
  session_id = None

  def to_dict(self):
    return {
      'id': self.id,
      'username': self.username,
      'profile_image_url': self.profile_image_url,
      'bio': self.bio,
      'active': self.active,
    }

bots_profiles = [
  Bot_Profile(-0, None, 'rando_man'),
]
