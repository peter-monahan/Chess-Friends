//all actions specific to COMMENTS Resource

//imports
import { myFetch } from "./myFetch";
import { deleteGameRequest } from "./gameRequests";

//constants
const GET_ALL_GAMES = 'games/GET_ALL_GAMES';
const CREATE_GAME = 'games/CREATE_GAME';
const DELETE_GAME = 'games/DELETE_GAME';


//ACTION CREATORS
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
    default:
      return state;
  };
};
