from .Pieces import pieces_obj
from .default_state import default

class Board:
  def __init__(self, game=None):
    data = None
    if game :
      data = game
    else:
      data = default



    # self.pieces_obj = pieces_obj

    self.grid = data['board']
    self.black_pieces = {id: pieces_obj[id[6:9]](self, data.black_pieces[id]) for id in data.black_pieces}
    self.black_king = self.black_pieces['black,king']
    self.white_pieces = {id: pieces_obj[id[6:9]](self, data.white_pieces[id]) for id in data.white_pieces}
    self.white_king = self.white_pieces['white,king']
    self.opponent_line_of_sight = []
    self.checks = [],
    self.pinned_pieces = {}

    self.turn = [data['turn'][1], data['turn'][0]]
    self.next_id = data['next_id']
    self.update()
    # for piece in self.white_pieces:
    #   piece.getValidMoves()



  # def populate(self, map):
  #   for  rowKey in map:
  #       col = map[rowKey]

  #       for colKey in col:
  #           [color, type] = col[colKey].split(',')
  #           piece = pieces_obj[type](self, color, [int(rowKey), int(colKey)])
  #           self.grid[rowKey][colKey] = f'{col[colKey]},{self.next_id}'

  #           if color == 'black':
  #             self.black_pieces[f'{col[colKey]},{self.next_id}'] = piece
  #             self.next_id += 1
  #           else:
  #             self.white_pieces[f'{col[colKey]},{self.next_id}'] = piece
  #             self.next_id += 1


  def update(self):
    [self.turn[0], self.turn[1]] = [self.turn[1], self.turn[0]]
    self.checks = []
    self.opponent_line_of_sight = []

    self.pinned_pieces = king.check_for_pins()

    king = self[f'{self.turn[0]}_king']
    [king_row, king_col] = king.curr_coords

    king_str = self.grid[king_row][king_col]
    self.grid[king_row][king_col] = None

    for piece in self[f'{self.turn[1]}_pieces']:
      piece_sight = piece.get_line_of_sight()

      for coord in piece_sight:
        square = ','.join(coord)
        self.opponent_line_of_sight.append(square)


    self.grid[king_row][king_col] = king_str
    for piece in self[f'{self.turn[0]}_pieces']:
      piece.get_valid_moves()

  def to_dict(self):
    return {
    'board': self.grid,
    'black_pieces': self.black_pieces,
    'white_pieces': self.white_pieces,
    'turn': self.turn,
    'next_id': self.next_id
    }
  # def select(self, coordStr):
  #   [row, col] = coordStr.split(',')

  #   string = self.grid[row][col]
  #   return "?"
