//all actions specific to COMMENTS Resource

//imports
import { myFetch } from "./myFetch";
import { deleteGameRequest } from "./gameRequests";

//constants
const GET_ALL_GAMES = 'games/GET_ALL_GAMES';
const CREATE_GAME = 'games/CREATE_GAME';
const DELETE_GAME = 'games/DELETE_GAME';
const MOVE_PIECE = 'games/MOVE_PIECE';


//ACTION CREATORS
const movePiece = (gameId, move) => {
  return {
    type: MOVE_PIECE,
    gameId,
    move
  }
};


const getGames = (games) => {
  return {
    type: GET_ALL_GAMES,
    games
  }
};


export const addGame = (game) => {
  return {
    type: CREATE_GAME,
    game
  }
};


export const deleteGame = (gameId) => {
  return {
    type: DELETE_GAME,
    gameId
  }
};

//Thunks

//GET ALL Comments
export const getAllGames = () => async (dispatch) => {
  const res = await myFetch(`/api/games`);
  if (res.ok) {
    const games = await res.json();
    dispatch(getGames(games));
  }
  return res;
};

export const getAGame = (gameId) => async (dispatch) => {
  const res = await myFetch(`/api/games/${gameId}`);
  if (res.ok) {
    const game = await res.json();
    dispatch(addGame(game));
  }
  return res;
};

//CREATE Comment
export const acceptGameRequest = (requestId) => async (dispatch) => {

  const res = await myFetch(`/api/games/requests/${requestId}`, {
    method: 'PUT'
  });

  if (res.ok) {
    const newGame = await res.json();
    dispatch(addGame(newGame));
    dispatch(deleteGameRequest(requestId, 'received'))
    return newGame.id
  }
};

export const createBotGame = (botId) => async (dispatch) => {

  const res = await myFetch(`/api/games/requests`, {
    method: 'POST',
    body: JSON.stringify({
      opponent_id: botId
    })
  });

  if (res.ok) {
    const newGame = await res.json();
    dispatch(addGame(newGame));
  }
};


//DELETE Comment
export const forfeiteGame = (gameId) => async (dispatch) => {
  const res = await myFetch(`/api/games/${gameId}`, {
    method: 'DELETE'
  });

  if (res.ok) {
    const game = await res.json();
    dispatch(addGame(game));
  }

};


export const makeAMove = (gameId, move) => async (dispatch) => {
  dispatch(movePiece(gameId, move))
  if (move.piece){
    await setTimeout(() => true, 400)
  }
  const res = await myFetch(`/api/games/${gameId}`, {
    method: 'PUT',
    body: JSON.stringify(move)
  });

  if (res.ok) {
    const game = await res.json();
    dispatch(addGame(game));
  } else {
    const response = res.json()
  }
};

const initialState = {};

//Comments REDUCER
export default function reducer(state = initialState, action) {
  let newState = {...state}
  switch (action.type) {
    case GET_ALL_GAMES:
      return action.games
    case CREATE_GAME:
      newState[action.game.id] = action.game
      return newState;
    case DELETE_GAME:
      delete newState[action.gameId]
      return newState;
    case MOVE_PIECE:
      newState[action.gameId] = {...newState[action.gameId], data: {...newState[action.gameId].data, pieces: { white: {...newState[action.gameId].data.pieces.white}, black: {...newState[action.gameId].data.pieces.black}}}}
      const [oldCoords, newCoords] = action.move.move;
      const gameData = newState[action.gameId].data;
      gameData.board = gameData.board.map(row => row.map(item => item))
      const pieceStr = gameData.board[oldCoords[0]][oldCoords[1]];
      const oldPieceStr = gameData.board[newCoords[0]][newCoords[1]];
      gameData.board[oldCoords[0]][oldCoords[1]] = null;
      gameData.board[newCoords[0]][newCoords[1]] = pieceStr;
      gameData.pieces[pieceStr.slice(0, 5)][pieceStr] = {...gameData.pieces[pieceStr.slice(0, 5)][pieceStr]}
      gameData.pieces[pieceStr.slice(0, 5)][pieceStr].curr_coords = newCoords
      if(oldPieceStr){
        delete gameData.pieces[oldPieceStr.slice(0, 5)][oldPieceStr];
      }
      gameData.turn = [gameData.turn[1], gameData.turn[0]];
      gameData.history = [...gameData.history].push(action.move.move)
      return newState;
    default:
      return state;
  };
};
