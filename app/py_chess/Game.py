from .Pieces import pieces_obj
from .default_state import default

class Game:
  def __init__(self, game=None):
    data = None
    if game :
      data = game
    else:
      data = default



    # self.pieces_obj = pieces_obj

    self.board = data['board']
    self.pieces = {
      'white': {id: pieces_obj[id[6:10]](self, data['pieces']['white'][id]) for id in data['pieces']['white']},
      'black': {id: pieces_obj[id[6:10]](self, data['pieces']['black'][id]) for id in data['pieces']['black']}
    }
    self.kings = {
      'white': self.pieces['white']['white,king,00'],
      'black': self.pieces['black']['black,king,00']
    }
    self.opponent_line_of_sight = []
    self.checks = []
    self.pinned_pieces = {}
    self.valid_moves = []
    self.turn = data['turn']
    self.next_id = data['next_id']
    self.history = data['history']
    self.forfeit = data['forfeit']
    self.winner = data['winner']
    self.checkmate = False
    self.stalemate = False



    # self.black_king = self.black_pieces['black,king']
    # self.white_king = self.white_pieces['white,king']
    # self.white_pieces = {id: pieces_obj[id[6:10]](self, data['white_pieces'][id]) for id in data['white_pieces']}
    # self.black_pieces = {id: pieces_obj[id[6:10]](self, data['black_pieces'][id]) for id in data['black_pieces']}



  def update(self):
    print('==========UPDATING BOARD')
    [self.turn[0], self.turn[1]] = [self.turn[1], self.turn[0]]
    self.checks = []
    self.opponent_line_of_sight = []
    self.valid_moves = []

    king = self.kings[self.turn[0]]
    enemy_pieces = self.pieces[self.turn[1]]
    friendly_pieces = self.pieces[self.turn[0]]
    self.pinned_pieces = king.check_for_pins()
    [king_row, king_col] = king.curr_coords
    self.board[king_row][king_col] = None

    for piece_key in enemy_pieces:
      piece_sight = enemy_pieces[piece_key].get_line_of_sight()
      enemy_pieces[piece_key].valid_moves = []

      for square in piece_sight:
        self.opponent_line_of_sight.append(square)

    self.board[king_row][king_col] = king.id
    for piece_key in friendly_pieces:
      friendly_pieces[piece_key].get_valid_moves()

    if not self.valid_moves:
      if self.checks:
        self.checkmate = True
        self.winner = self.turn[1]
      else:
        self.stalemate = True

  def to_dict(self):
    return {
    'board': self.board,
    'pieces': {
      'black': {self.pieces['black'][key].id: self.pieces['black'][key].to_dict() for key in self.pieces['black']},
      'white': {self.pieces['white'][key].id: self.pieces['white'][key].to_dict() for key in self.pieces['white']},
    },
    'turn': self.turn,
    'next_id': self.next_id,
    'stalemate': self.stalemate,
    'checkmate': self.checkmate,
    'checks': self.checks,
    'history': self.history,
    'forfeit': self.forfeit,
    'winner': self.winner
    }

  def move(self, old_coords, new_coords):
    if self.checkmate or self.stalemate or self.forfeit:
      return False
    id = self.board[old_coords[0]][old_coords[1]]
    if id[:5] != self.turn[0]:
      return False

    piece = self.pieces[self.turn[0]][id]

    if new_coords in piece.valid_moves:
      piece.move(new_coords)
      self.history.append([old_coords, new_coords])
      return True
    else:
      return False

  def forfeit_game(self, color):
    if color == 'black':
      self.forfeit = color
      self.winner = 'white'
    elif color == 'white':
      self.forfeit = color
      self.winner = 'black'
    else :
      raise ValueError("color must be either 'black' or 'white'")
  # def select(self, coordStr):
  #   [row, col] = coordStr.split(',')

  #   string = self.board[row][col]
  #   return "?"


  # def populate(self, map):
  #   for  rowKey in map:
  #       col = map[rowKey]

  #       for colKey in col:
  #           [color, type] = col[colKey].split(',')
  #           piece = pieces_obj[type](self, color, [int(rowKey), int(colKey)])
  #           self.board[rowKey][colKey] = f'{col[colKey]},{self.next_id}'

  #           if color == 'black':
  #             self.black_pieces[f'{col[colKey]},{self.next_id}'] = piece
  #             self.next_id += 1
  #           else:
  #             self.white_pieces[f'{col[colKey]},{self.next_id}'] = piece
  #             self.next_id += 1
