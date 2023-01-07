from .Pieces import pieces_obj
from .default_state import default

class Game:
  def __init__(self, game=None, prev_state=None):
    if prev_state:
      self.board = prev_state.board
      self.pieces = {
        'white': {id: pieces_obj[id[6:10]](self, prev_state['pieces']['white'][id]) for id in prev_state['pieces']['white']},
        'black': {id: pieces_obj[id[6:10]](self, prev_state['pieces']['black'][id]) for id in prev_state['pieces']['black']}
      }
      self.kings = {
        'white': self.pieces['white']['white,king,00'],
        'black': self.pieces['black']['black,king,00']
      }
      self.opponent_line_of_sight = []
      self.checks = []
      self.pinned_pieces = {}
      self.valid_moves = prev_state['valid_moves']
      self.turn = prev_state['turn']
      self.next_id = prev_state['next_id']
      self.history = []
      self.forfeit = prev_state['forfeit']
      self.winner = prev_state['winner']
      self.checkmate = False
      self.stalemate = False
    else:
      if game :
        data = game
      else:
        data = {**default}
        data['board'] = [[item for item in row] for row in default['board']]
        data['history'] = []
        data['turn'] = ['white', 'black']



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
      self.valid_moves = data['valid_moves']
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
    self.valid_moves = {}

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

  def to_passable_dict(self):
    return {
    'board': [[square for square in row] for row in self.board],
    'pieces': {
      'black': {self.pieces['black'][key].id: self.pieces['black'][key].to_dict() for key in self.pieces['black']},
      'white': {self.pieces['white'][key].id: self.pieces['white'][key].to_dict() for key in self.pieces['white']},
    },
    'turn': [*self.turn],
    'next_id': self.next_id,
    'stalemate': self.stalemate,
    'checkmate': self.checkmate,
    'checks': self.checks,
    'forfeit': self.forfeit,
    'winner': self.winner,
    'valid_moves': self.valid_moves
    }

  def move(self, move):
    if self.checkmate or self.stalemate or self.forfeit:
      raise RuntimeError(f'Cannot make move if checkmate, stalemate, or forfeit is true...  checkmate:{self.checkmate}, stalemate:{self.stalemate}, forfeit:{self.forfeit}')
      return False
    [old_coords, new_coords] = move['move']
    id = self.board[old_coords[0]][old_coords[1]]
    if id[:5] != self.turn[0]:
      raise RuntimeError(f'Cannot move piece if color is not equal to current turn color...  id:{id}, turn:{self.turn[0]}')
      return False

    piece = self.pieces[self.turn[0]][id]

    if new_coords in piece.valid_moves:
      if (id[:10] == 'white,pawn' and new_coords[0] == 0) or (id[:10] == 'black,pawn' and new_coords[0] == 7):
        if not move.get('piece'):
          move['piece'] = 'queen'
        old_piece_str = self.board[new_coords[0]][new_coords[1]]
        if old_piece_str:
          del self.pieces[old_piece_str[:5]][old_piece_str]
        new_id = f'{self.turn[0]},{move.get("piece")},{str(self.next_id)}'
        self.next_id += 1
        data = {
          'id': new_id,
          'color': self.turn[0],
          'curr_coords': new_coords,
          'times_moved': 0,
          'valid_moves': []
        }
        self.pieces[self.turn[0]][new_id] = pieces_obj[move["piece"][:4]](self, data)
        del self.pieces[self.turn[0]][id]
        self.board[new_coords[0]][new_coords[1]] = new_id
        self.board[old_coords[0]][old_coords[1]] = None
      else:
        piece.move(new_coords, piece=piece)


      self.history.append([old_coords, new_coords])

      self.update()
      return True
    else:
      raise RuntimeError(f'Cannot move piece if move is not in piece valid moves...  new_coords:{new_coords}, valid_moves:{piece.valid_moves} piece:{piece.to_dict()}')
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

  def evaluate_score(self):
    white_score = 0
    black_score = 0

    for pieceKey in self.pieces['white']:
      white_score += self.pieces['white'][pieceKey].get_value()

    for pieceKey in self.pieces['black']:
      black_score -= self.pieces['black'][pieceKey].get_value()

    return white_score + black_score


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
    'winner': self.winner,
    'valid_moves': self.valid_moves,
    'score': self.evaluate_score()
    }
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
