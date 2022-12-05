class Piece:
  def __init__(self, game, data):
    self.game = game
    self.color = data['color']
    # self.start_coords = start_coords
    self.curr_coords = data['curr_coords']
    self.times_moved = data['times_moved']
    self.valid_moves = data['valid_moves']
    self.id = data['id']


  def to_dict(self):
    return {
      'id': self.id,
      'color': self.color,
      'curr_coords': self.curr_coords,
      'times_moved': self.times_moved,
      'valid_moves': self.valid_moves
    }

  def move(self, new_coords):
    [curr_row, curr_col] = self.curr_coords
    [new_row, new_col] = new_coords
    old_piece = self.game.board[new_row][new_col]

    if old_piece:
      del self.game.pieces[old_piece[:5]][old_piece]


    self.game.board[curr_row][curr_col] = None
    self.game.board[new_row][new_col] = self.id
    self.curr_coords = new_coords
    self.times_moved += 1
    self.game.update()
    return False


  def get_valid_moves(self):
    res = []
    visible_squares = self.get_line_of_sight()

    for square in visible_squares:
      [row, col] = square
      if self.game.board[row][col]:
        if self.game.board[row][col][:5] != self.color:
          res.append(square)
      else:
        res.append(square)

    if self.game.checks:
      if len(self.game.checks) > 1:
        res = []
      else:
          valid = self.game.checks[0]
          res = [square for square in res if square in valid]


    if self.game.pinned_pieces.get(','.join([str(num) for num in self.curr_coords])):
      res = [square for square in res if square in self.game.pinned_pieces[','.join([str(num) for num in self.curr_coords])]]

    self.valid_moves = res
    self.game.valid_moves.extend(res)
    return res



class LongRangePiece(Piece):
  def __init__(self, game, data):
    super().__init__(game, data)


  def get_line_of_sight(self):
    res = []

    for direction in self.directions:
      [rowDir, colDir] = direction
      [row, col] = self.curr_coords
      checkArr = [[row, col]]
      currEl = None

      while row+rowDir in range(8) and col+colDir in range(8) and (currEl is None):
        row += rowDir
        col += colDir

        currEl = self.game.board[row][col]
        res.append([row, col])
        if self.game.turn[1] == self.color:
          if self.color == 'white':
            enemy_king = self.game.kings['black']
          else:
            enemy_king = self.game.kings['white']

          if [row, col] == enemy_king.curr_coords:
            self.game.checks.append(checkArr)
        else:
            checkArr.append([row,col])

    return res



class ShortRangePiece(Piece):
  def __init__(self, game, data):
    super().__init__(game, data)


  def get_line_of_sight(self):
    res = []
    [curr_row, curr_col] = self.curr_coords
    if self.color == 'white':
      enemy_king = self.game.kings['black']
    else:
      enemy_king = self.game.kings['white']
    for pair in self.pairs:
      [row, col] = pair
      row+=curr_row
      col+=curr_col

      if((row <= 7 and row >= 0) and (col <= 7 and col >= 0)):
        if ((self.game.turn[1] == self.color) and ([row, col] == enemy_king.curr_coords)):
          self.game.checks.append([curr_row,curr_col])

        res.append([row, col])

    return res







class Pawn(ShortRangePiece):
  def __init__(self, game, data):
    super().__init__(game, data)

    self.en_passantable = data['en_passantable']
    self.double_move = data['double_move']
    self.en_passant_move = data['en_passant_move']
    if self.color == 'black':
      self.pairs = [[1, -1], [1, 1]]
    elif self.color == 'white':
      self.pairs = [[-1, -1], [-1, 1]]


  def to_dict(self):
    return {
      'id': self.id,
      'color': self.color,
      'curr_coords': self.curr_coords,
      'times_moved': self.times_moved,
      'valid_moves': self.valid_moves,
      'en_passantable': self.en_passantable,
      'double_move': self.double_move,
      'en_passant_move': self.en_passant_move
    }


  def move(self, new_coordinates):
    upgrade_bool = False
    [curr_row, curr_col] = self.curr_coords
    [new_row, new_col] = new_coordinates
    old_piece = None
    old_piece_key = None
    if new_coordinates == self.double_move:
      self.en_passantable = True
    elif self.en_passant_move.get(','.join([str(num) for num in new_coordinates ])):
      old_piece_key = self.en_passant_move[','.join([str(num) for num in new_coordinates ])]
      old_piece = self.game.pieces[old_piece_key[:5]][old_piece_key]
      [oldRow, oldCol] = old_piece.curr_coords
      self.game.board[oldRow][oldCol] = None
    else:
      old_piece_key = self.game.board[new_row][new_col]
      if old_piece_key:
        old_piece = self.game.pieces[old_piece_key[:5]][old_piece_key]


    if (old_piece):
      del self.game.pieces[old_piece_key[:5]][old_piece_key]


    self.game.board[curr_row][curr_col] = None
    self.game.board[new_row][new_col] = self.id
    self.curr_coords = new_coordinates
    self.times_moved += 1

    if self.color == 'white' and self.curr_coords[0] == 0:
      upgrade_bool = True
    elif self.color == 'black' and self.curr_coords[0] == 7:
      upgrade_bool = True

    self.game.update()
    return upgrade_bool


  def get_valid_moves(self):
    self.double_move = None
    self.en_passant_move = {}
    if self.color == self.game.turn[0]:
      self.en_passantable = False


    res = []
    visible_squares = self.get_line_of_sight()
    [curr_row, curr_col] = self.curr_coords
    first_square = None
    second_square = None
    if self.color == 'black':
      first_square = 1
      second_square = 2
    elif self.color == 'white':
      first_square = -1
      second_square = -2


    if self.game.board[curr_row+first_square][curr_col] == None:
      res.append([curr_row+first_square, curr_col])
      if self.times_moved == 0 and self.game.board[curr_row+second_square][curr_col] == None:
        res.append([curr_row+second_square, curr_col])
        self.double_move = [curr_row+second_square,curr_col]

    for square in visible_squares:
      [row, col] = square
      piece1 = self.game.board[row][col]
      piece2 = self.game.board[curr_row][col]
      if piece1 and piece1[:5] != self.color:
        res.append(square)

      elif piece2 and piece2[6:10] == 'pawn' and piece2[:5] != self.color and self.game.pieces[piece2[:5]][piece2].__getattribute__('en_passantable'):
        res.append(square)
        self.en_passant_move[','.join([str(num) for num in square])] = self.game.board[curr_row][col]


    if self.game.checks:
      if len(self.game.checks) > 1:
        res = []
      else:
        valid = self.game.checks[0]
        res = [square for square in res if square in valid]


    if self.game.pinned_pieces.get(','.join([str(num) for num in self.curr_coords])):
      res = [square for square in res if square in self.game.pinned_pieces[','.join([str(num) for num in self.curr_coords])]]


    self.valid_moves = res
    self.game.valid_moves.extend(res)
    return res

class Rook(LongRangePiece):
  def __init__(self, game, data):
    super().__init__(game, data)

    self.directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]

class Knight(ShortRangePiece):
  def __init__(self, game, data):
    super().__init__(game, data)

    self.pairs = [[-2, -1], [-2, 1], [-1, -2], [1, -2], [-1, 2], [1, 2], [2, -1], [2, 1]]


class Bishop(LongRangePiece):
  def __init__(self, game, data):
    super().__init__(game, data)

    self.directions = [[1,-1], [1, 1], [-1, -1], [-1, 1]]


class Queen(LongRangePiece):
  def __init__(self, game, data):
    super().__init__(game, data)

    self.directions = [[-1, 0], [1, 0], [0, -1], [0, 1], [1,-1], [1, 1], [-1, -1], [-1, 1]]


class King(ShortRangePiece):
  def __init__(self, game, data):
    super().__init__(game, data)

    self.castle_move = data['castle_move']
    if self.color == 'white':
      self.game.white_king = self
    else:
      self.game.black_king = self
    self.pairs = [[1,-1], [1, 1], [-1, -1], [-1, 1], [-1, 0], [1, 0], [0, -1], [0, 1]]


  def to_dict(self):
    return {
      'id': self.id,
      'color': self.color,
      'curr_coords': self.curr_coords,
      'times_moved': self.times_moved,
      'valid_moves': self.valid_moves,
      'castle_move': self.castle_move
    }

  def move(self, new_coordinates):
    [curr_row, curr_col] = self.curr_coords
    [new_row, new_col] = new_coordinates
    old_piece = self.game.board[new_row][new_col]

    if self.castle_move.get(','.join([str(num) for num in new_coordinates])):
      rook = self.castle_move[','.join([str(num) for num in new_coordinates])]['piece']
      [rookRow, rookCol] = self.castle_move[','.join([str(num) for num in new_coordinates])]['spot']
      [oldRookRow, oldRookCol] = rook.curr_coords

      self.game.board[oldRookRow][oldRookCol] = None
      self.game.board[rookRow][rookCol] = rook
      rook.curr_coords = self.castle_move[','.join([str(num) for num in new_coordinates])].spot
      rook.times_moved += 1


    if old_piece:
      del self.game.pieces[old_piece[:5]][old_piece]



    self.game.board[curr_row][curr_col] = None
    self.game.board[new_row][new_col] = self.id
    self.curr_coords = new_coordinates
    self.times_moved += 1
    self.game.update()
    return False


  def get_valid_moves(self):
    self.castle_move = {}
    res = []
    visible_squares = self.get_line_of_sight()

    friendly_pieces = self.game.pieces[self.color]

    for square in visible_squares:
      [row, col] = square
      if not (self.game.board[row][col]) or (self.game.board[row][col][:5] != self.color):
        res.append(square)

    res = [square for square in res if not (square in self.game.opponent_line_of_sight)]

    if self.times_moved == 0:
      leftRight = [-1, 1]

      for direction in leftRight:
        [row, col] = self.curr_coords
        castle_move = f'{row},{(direction * 2) + col}'
        dependantMove = f'{row},{direction + col}'
        foundPiece = None

        while col+direction in range(8) and  not foundPiece:
          col += direction

          if self.game.board[row][col]:
            pieceStr = self.game.board[row][col]
            foundPiece = friendly_pieces.get(pieceStr)


        if foundPiece and foundPiece.id[6:10] == 'rook' and foundPiece.times_moved == 0:
          if dependantMove in res and not (castle_move in self.game.opponent_line_of_sight):
            self.castle_move[castle_move] = {'piece': foundPiece, 'spot': [int(num) for num in dependantMove.split(',')]}
            res.append(castle_move)


    self.valid_moves = res
    self.game.valid_moves.extend(res)
    return res


  def check_for_pins(self):
    pairs = [[['bish', 'quee'], [[1,-1], [1, 1], [-1, -1], [-1, 1]]], [['rook', 'quee'], [[-1, 0], [1, 0], [0, -1], [0, 1]]]]
    res = {}

    for pair in pairs:
      [threats, directions] = pair
      for direction in directions:
        [rowDir, colDir] = direction
        [row, col] = self.curr_coords
        pinnedMoves = []
        pieces = []


        while row+rowDir in range(8) and col+colDir in range(8) and len(pieces) < 2:
          row += rowDir
          col += colDir

          pinnedMoves.append(f'{row},{col}')

          if self.game.board[row][col]:
            pieces.append(self.game.board[row][col])


        if (len(pieces) == 2) and (pieces[0][:5] == self.color) and (pieces[1][:5] != self.color) and (pieces[1][6:10] in threats):
          res[','.join([str(num) for num in self.game.pieces[self.color][pieces[0]].curr_coords])] = pinnedMoves

    return res

pieces_obj = {
  'pawn': Pawn,
  'rook': Rook,
  'knig': Knight,
  'bish': Bishop,
  'quee': Queen,
  'king': King
}
