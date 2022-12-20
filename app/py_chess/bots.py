from .Game import Game
import random
def rando_man(game):
  keys = game.valid_moves.keys
  choiceKey = random.choice(keys)
  chosen_coords = random.choice(game.valid_moves[choiceKey])

  return [[int(num) for num in choiceKey.split(',')], chosen_coords]

bots = {
  1: rando_man
}
