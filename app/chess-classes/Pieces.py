class Piece:
  def __init__(self, board, data):
    self.board = board
    self.color = data['id'][:5]
    # self.start_coords = start_coords
    self.curr_coords = data['curr_coords']
    self.times_moved = data['times_moved']
    self.valid_moves = data['valid_moves']
    self.id = data['id']


  def move(self, new_coords):
    [curr_row, curr_col] = self.curr_coords
    [new_row, new_col] = new_coords
    old_piece = self.board.grid[new_row][new_col]

    if old_piece:
      del self.board[f'{old_piece[:5]}_pieces'][old_piece]


    self.board.grid[curr_row][curr_col] = None
    self.board.grid[new_row][new_col] = self.id
    self.curr_coords = new_coords
    self.times_moved += 1
    return False


  def get_valid_moves(self):
    res = []
    visible_squares = self.get_line_of_sight()

    for square in visible_squares:
      [row, col] = square
      if self.board.grid[row][col]:
        if self.board.grid[row][col][:5] != self.color:
          res.append(','.join(square))
    else:
        res.append(','.join(square))

    if len(self.board.checks):
      if len(self.board.checks.length) > 1:
        res = []
    else:
        valid = self.board.checks[0]
        res = [square for square in res if square in valid]


    if self.board.pinned_pieces[self.curr_coords.join(',')]:
      res = [square for square in res if square in self.board.pinned_pieces[self.curr_coords.join(',')]]

    self.valid_moves = res
    return res



class LongRangePiece(Piece):
  def __init__(self, board, data):
    super().__init__(board, data)


  def get_line_of_sight(self):
    res = []

    for direction in self.directions:
      [rowDir, colDir] = direction
      [row, col] = self.curr_coords
      checkArr = [f'{row},{col}']
      currEl = None

      while row+rowDir in range(8) and col+colDir in range(8) and (currEl is None):
        row += rowDir
        col += colDir

        currEl = self.board.grid[row][col]
        res.append([row, col])
        if self.board.turn[1] == self.color:
          if f'{row},{col}' == self.board[f'{self.board.turn[0]}_king'].curr_coords.join(','):
            self.board.checks.append(checkArr)
        else:
            checkArr.append(f'{row},{col}')

    return res



class ShortRangePiece(Piece):
  def __init__(self, board, data):
    super().__init__(board, data)


  def get_line_of_sight(self):
    res = []
    [curr_row, curr_col] = self.curr_coords

    for pair in self.pairs:
      [row, col] = pair
      row+=curr_row
      col+=curr_col

      if((row <= 7 and row >= 0) and (col <= 7 and col >= 0)):
        if ((self.board.turn[1] == self.color) and (f'{row},{col}' == ','.join(self.board[f'{self.board.turn[0]}_king'].curr_coords))):
          self.board.checks.append([f'{curr_row},{curr_col}'])

        res.append([row, col])

    return res







class Pawn(ShortRangePiece):
  def __init__(self, board, data):
    super().__init__(board, data)

    self.en_passantable = False
    self.double_move = None
    self.en_passant_move = {}
    if self.color == 'black':
      self.pairs = [[1, -1], [1, 1]]
    elif self.color == 'white':
      self.pairs = [[-1, -1], [-1, 1]]



  def move(self, new_coordinates):
    upgrade_bool = False
    [curr_row, curr_col] = self.curr_coords
    [new_row, new_col] = new_coordinates
    old_piece = None

    if new_coordinates.join(',') == self.double_move:
      self.en_passantable = True
    elif self.en_passant_move[new_coordinates.join(',')]:
      old_piece = self.en_passant_move[new_coordinates.join(',')]
      [oldRow, oldCol] = old_piece.curr_coords
      self.board.grid[oldRow][oldCol] = None
    else:
      old_piece = self.board.grid[new_row][new_col]


    if (old_piece):
      del self.board[f'{old_piece[:5]}_pieces'][old_piece]


    self.board.grid[curr_row][curr_col] = None
    self.board.grid[new_row][new_col] = self.id
    self.curr_coords = new_coordinates
    self.times_moved += 1

    if self.color == 'white' and self.curr_coords[0] == 0:
      upgrade_bool = True
    elif self.color == 'black' and self.curr_coords[0] == 7:
      upgrade_bool = True


    return upgrade_bool


  def get_valid_moves(self):
    self.double_move = None
    self.en_passant_move = {}
    if self.color == self.board.turn[0]:
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


    if self.board.grid[curr_row+first_square][curr_col] == None:
      res.append(','.join([curr_row+first_square, curr_col]))
      if self.times_moved == 0 and self.board.grid[curr_row+second_square][curr_col] == None:
        res.append(','.join([curr_row+second_square, curr_col]))
        self.double_move = f'{curr_row+second_square},{curr_col}'

    for square in visible_squares:
      [row, col] = square
      piece1 = self.board.grid[row][col]
      piece2 = self.board.grid[curr_row][col]
      if piece1 and piece1[:5] != self.color:
        res.append(','.join(square))

      elif piece2 and piece2[:5] != self.color and self.board[f'{piece2[:5]}_pieces'][piece2].en_passantable:
        res.append(','.join(square))
        self.en_passant_move[','.join(square)] = self.board.grid[curr_row][col]


    if self.board.checks:
      if len(self.board.checks) > 1:
        res = []
      else:
        valid = self.board.checks[0]
        res = [square for square in res if square in valid]


    if self.board.pinned_pieces[','.join(self.curr_coords)]:
      res = [square for square in res if square in self.board.pinned_pieces[','.join(self.curr_coords)]]


    self.valid_moves = res
    return res

class Rook(LongRangePiece):
  def __init__(self, board, data):
    super().__init__(board, data)

    self.directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]

class Knight(ShortRangePiece):
  def __init__(self, board, data):
    super().__init__(board, data)

    self.pairs = [[-2, -1], [-2, 1], [-1, -2], [1, -2], [-1, 2], [1, 2], [2, -1], [2, 1]]


class Bishop(LongRangePiece):
  def __init__(self, board, data):
    super().__init__(board, data)

    self.directions = [[1,-1], [1, 1], [-1, -1], [-1, 1]]


class Queen(LongRangePiece):
  def __init__(self, board, data):
    super().__init__(board, data)

    self.directions = [[-1, 0], [1, 0], [0, -1], [0, 1], [1,-1], [1, 1], [-1, -1], [-1, 1]]


class King(ShortRangePiece):
  def __init__(self, board, data):
    super().__init__(board, data)

    self.castleMove = {}
    self.board[f'{id[:5]}_king'] = self
    self.pairs = [[1,-1], [1, 1], [-1, -1], [-1, 1], [-1, 0], [1, 0], [0, -1], [0, 1]]


  def move(self, new_coordinates):
    [curr_row, curr_col] = self.curr_coords
    [new_row, new_col] = new_coordinates
    old_piece = self.board.grid[new_row][new_col]

    if self.castleMove[','.join(new_coordinates)]:
      rook = self.castleMove[','.join(new_coordinates)]['piece']
      [rookRow, rookCol] = self.castleMove[','.join(new_coordinates)]['spot']
      [oldRookRow, oldRookCol] = rook.curr_coords

      self.board.grid[oldRookRow][oldRookCol] = None
      self.board.grid[rookRow][rookCol] = rook
      rook.curr_coords = self.castleMove[','.join(new_coordinates)].spot
      rook.times_moved += 1


    if old_piece:
      del self.board[f'{old_piece[:5]}_pieces'][old_piece]



    self.board.grid[curr_row][curr_col] = None
    self.board.grid[new_row][new_col] = self.id
    self.curr_coords = new_coordinates
    self.times_moved += 1
    return False


  def get_valid_moves(self):
    self.castleMove = {}
    res = []
    visible_squares = self.get_line_of_sight()

    for square in visible_squares:
      [row, col] = square
      if not (self.board.grid[row][col]) or (self.board.grid[row][col][:5] != self.color):
        res.append(','.join(square))

    res = [square for square in res if not (square in self.board.opponent_line_of_sight)]

    if self.times_moved == 0:
      leftRight = [-1, 1]

      for direction in leftRight:
        [row, col] = self.curr_coords
        castleMove = f'{row},{(direction * 2) + col}'
        dependantMove = f'{row},{direction + col}'
        foundPiece = None

        while col+direction in range(8) and  not foundPiece:
          col += direction

          if self.board.grid[row][col]:
            pieceStr = self.board.grid[row][col]
            foundPiece = self.board[f'{pieceStr[:5]}_pieces'][pieceStr]


        if foundPiece and foundPiece.id[6:10] == 'rook' and foundPiece.times_moved == 0:
          if dependantMove in res and not (castleMove in self.board.opponent_line_of_sight):
            self.castleMove[castleMove] = {'piece': foundPiece, 'spot': [int(num) for num in dependantMove.split(',')]}
            res.append(castleMove)


    self.valid_moves = res
    return res


  def checkForPins(self):
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

          if self.board.grid[row][col]:
            pieces.append(self.board.grid[row][col])


        if (len(pieces) == 2) and (pieces[0][:5] == self.color) and (pieces[1][:5] != self.color) and (pieces[1][6:10] in threats):
          res[','.join(self.board[f'{self.color}_pieces'][pieces[0]].curr_coords)] = pinnedMoves

    return res
