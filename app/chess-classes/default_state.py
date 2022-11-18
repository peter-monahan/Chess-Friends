default = {
  'next_id': 15,
  'turn': ['white', 'black'],
  'board': [
    ['black,rook,1', 'black,knight,2', 'black,bishop,3', 'black,queen,4', 'black,king', 'black,bishop,5', 'black,knight,6', 'black,rook,7'],
    ['black,pawn,8', 'black,pawn,9', 'black,pawn,10', 'black,pawn,11', 'black,pawn,12', 'black,pawn,13', 'black,pawn,14', 'black,pawn,15'],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ['white,pawn,8', 'white,pawn,9', 'white,pawn,10', 'white,pawn,11', 'white,pawn,12', 'white,pawn,13', 'white,pawn,14', 'white,pawn,15'],
    ['white,rook,1', 'white,knight,2', 'white,bishop,3', 'white,queen,4', 'white,king', 'white,bishop,5', 'white,knight,6', 'white,rook,7']
  ],
  'white_pieces': {
    'white,rook,1': {
      'id': 'white,rook,1',
      'valid_moves': [],
      'curr_coords': [7,0],
      'times_moved': 0
    },
    'white,knight,2': {
      'id': 'white,knight,2',
      'valid_moves': ["5,0","5,2"],
      'curr_coords': [7,1],
      'times_moved': 0
    },
    'white,bishop,3': {
      'id': 'white,bishop,3',
      'valid_moves': [],
      'curr_coords': [7,2],
      'times_moved': 0
    },
    'white,queen,4': {
      'id': 'white,queen,4',
      'valid_moves': [],
      'curr_coords': [7,3],
      'times_moved': 0
    },
    'white,king': {
      'id': 'white,king',
      'valid_moves': [],
      'curr_coords': [7,4],
      'times_moved': 0
    },
    'white,bishop,5': {
      'id': 'white,bishop,5',
      'valid_moves': [],
      'curr_coords': [7,5],
      'times_moved': 0
    },
    'white,knight,6': {
      'id': 'white,knight,6',
      'valid_moves': ["5,5","5,7"],
      'curr_coords': [7,6],
      'times_moved': 0
    },
    'white,rook,7': {
      'id': 'white,rook,7',
      'valid_moves': [],
      'curr_coords': [7,7],
      'times_moved': 0
    },
    'white,pawn,8': {
      'id': 'white,pawn,8',
      'valid_moves': ["5,0","4,0"],
      'curr_coords': [6,0],
      'times_moved': 0,
      "enPassantable": False,
      "doubleMove": "4,0",
      "enPassantMove": {},
    },
    'white,pawn,9': {
      'id': 'white,pawn,9',
      'valid_moves': ["5,1","4,1"],
      'curr_coords': [6,1],
      'times_moved': 0,
      "enPassantable": False,
      "doubleMove": "4,1",
      "enPassantMove": {},
    },
    'white,pawn,10': {
      'id': 'white,pawn,10',
      'valid_moves': ["5,2","4,2"],
      'curr_coords': [6,2],
      'times_moved': 0,
      "enPassantable": False,
      "doubleMove": "4,2",
      "enPassantMove": {},
    },
    'white,pawn,11': {
      'id': 'white,pawn,11',
      'valid_moves': ["5,3","4,3"],
      'curr_coords': [6,3],
      'times_moved': 0,
      "enPassantable": False,
      "doubleMove": "4,3",
      "enPassantMove": {},
    },
    'white,pawn,12': {
      'id': 'white,pawn,12',
      'valid_moves': ["5,4","4,4"],
      'curr_coords': [6,4],
      'times_moved': 0,
      "enPassantable": False,
      "doubleMove": "4,4",
      "enPassantMove": {},
    },
    'white,pawn,13': {
      'id': 'white,pawn,13',
      'valid_moves': ["5,5","4,5"],
      'curr_coords': [6,5],
      'times_moved': 0,
      "enPassantable": False,
      "doubleMove": "4,5",
      "enPassantMove": {},
    },
    'white,pawn,14': {
      'id': 'white,pawn,14',
      'valid_moves': ["5,6","4,6"],
      'curr_coords': [6,6],
      'times_moved': 0,
      "enPassantable": False,
      "doubleMove": "4,6",
      "enPassantMove": {},
    },
    'white,pawn,15': {
      'id': 'white,pawn,15',
      'valid_moves': ["5,7","4,7"],
      'curr_coords': [6,7],
      'times_moved': 0,
      "enPassantable": False,
      "doubleMove": "4,7",
      "enPassantMove": {},
    },
  },
  'black_pieces': {
    'black,rook,1': {
      'id': 'black,rook,1',
      'valid_moves': [],
      'curr_coords': [0,0],
      'times_moved': 0
    },
    'black,knight,2': {
      'id': 'black,knight,2',
      'valid_moves': ["2,0","2,2"],
      'curr_coords': [0,1],
      'times_moved': 0
    },
    'black,bishop,3': {
      'id': 'black,bishop,3',
      'valid_moves': [],
      'curr_coords': [0,2],
      'times_moved': 0
    },
    'black,queen,4': {
      'id': 'black,queen,4',
      'valid_moves': [],
      'curr_coords': [0,3],
      'times_moved': 0
    },
    'black,king': {
      'id': 'black,king',
      'valid_moves': [],
      'curr_coords': [0,4],
      'times_moved': 0
    },
    'black,bishop,5': {
      'id': 'black,bishop,5',
      'valid_moves': [],
      'curr_coords': [0,5],
      'times_moved': 0
    },
    'black,knight,6': {
      'id': 'black,knight,6',
      'valid_moves': ["2,5","2,7"],
      'curr_coords': [0,6],
      'times_moved': 0
    },
    'black,rook,7': {
      'id': 'black,rook,7',
      'valid_moves': [],
      'curr_coords': [0,7],
      'times_moved': 0
    },
    'black,pawn,8': {
      'id': 'black,pawn,8',
      'valid_moves': ["2,0","3,0"],
      'curr_coords': [6,0],
      'times_moved': 0,
      "enPassantable": False,
      "doubleMove": "3,0",
      "enPassantMove": {},
    },
    'black,pawn,9': {
      'id': 'black,pawn,9',
      'valid_moves': ["2,1","3,1"],
      'curr_coords': [6,1],
      'times_moved': 0,
      "enPassantable": False,
      "doubleMove": "3,1",
      "enPassantMove": {},
    },
    'black,pawn,10': {
      'id': 'black,pawn,10',
      'valid_moves': ["2,2","3,2"],
      'curr_coords': [6,2],
      'times_moved': 0,
      "enPassantable": False,
      "doubleMove": "3,2",
      "enPassantMove": {},
    },
    'black,pawn,11': {
      'id': 'black,pawn,11',
      'valid_moves': ["2,3","3,3"],
      'curr_coords': [6,3],
      'times_moved': 0,
      "enPassantable": False,
      "doubleMove": "3,3",
      "enPassantMove": {},
    },
    'black,pawn,12': {
      'id': 'black,pawn,12',
      'valid_moves': ["2,4","3,4"],
      'curr_coords': [6,4],
      'times_moved': 0,
      "enPassantable": False,
      "doubleMove": "3,4",
      "enPassantMove": {},
    },
    'black,pawn,13': {
      'id': 'black,pawn,13',
      'valid_moves': ["2,5","3,5"],
      'curr_coords': [6,5],
      'times_moved': 0,
      "enPassantable": False,
      "doubleMove": "3,5",
      "enPassantMove": {},
    },
    'black,pawn,14': {
      'id': 'black,pawn,14',
      'valid_moves': ["2,6","3,6"],
      'curr_coords': [6,6],
      'times_moved': 0,
      "enPassantable": False,
      "doubleMove": "3,6",
      "enPassantMove": {},
    },
    'black,pawn,15': {
      'id': 'black,pawn,15',
      'valid_moves': ["2,7","3,7"],
      'curr_coords': [6,7],
      'times_moved': 0,
      "enPassantable": False,
      "doubleMove": "3,7",
      "enPassantMove": {},
    },
  }
  }
