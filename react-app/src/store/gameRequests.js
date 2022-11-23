//all actions specific to COMMENTS Resource

//imports
import { myFetch } from "./myFetch";

//constants
const GET_ALL_GAME_REQUESTS = 'gameRequests/GET_ALL_GAME_REQUESTS';
const CREATE_GAME_REQUEST = 'gameRequests/CREATE_GAME_REQUEST';
const DELETE_GAME_REQUEST = 'gameRequests/DELETE_GAME_REQUEST';


//ACTION CREATORS
const getGameRequests = (gameRequests) => {
  return {
    type: GET_ALL_GAME_REQUESTS,
    gameRequests
  }
};


export const addGameRequest = (gameRequest, requestType) => {
  return {
    type: CREATE_GAME_REQUEST,
    gameRequest,
    requestType,
  }
};


const deleteGameRequest = (gameRequestId, requestType) => {
  return {
    type: DELETE_GAME_REQUEST,
    gameRequestId,
    requestType,
  }
};

//Thunks

//GET ALL Comments
export const getAllGameRequests = () => async (dispatch) => {
  const res = await myFetch(`/api/games/requests`);
  if (res.ok) {
    const gameRequests = await res.json();
    dispatch(getGameRequests(gameRequests));
  }
  return res;
};

//CREATE Comment
export const createGameRequest = (opponent_id) => async (dispatch) => {

  const res = await myFetch(`/api/games/requests`, {
    method: 'POST',
    body: JSON.stringify({
      opponent_id
    })
  });

  if (res.ok) {
    const newGameRequest = await res.json();
    dispatch(addGameRequest(newGameRequest, 'sent'));
    return res
  }
};


//DELETE Comment
export const deleteAGameRequest = (gameRequestId) => async (dispatch) => {
  const res = await myFetch(`/api/games/requests/${gameRequestId}`, {
    method: 'DELETE'
  });
  const response = await res.json();
  if (res.ok) {
    dispatch(deleteGameRequest(gameRequestId, response.requestType));
  }
  return response;
};


const initialState = {sent: {}, received: {}};

//Comments REDUCER
export default function reducer(state = initialState, action) {
  let newState = {sent:{...state.sent}, received: {...state.received}}
  switch (action.type) {
    case GET_ALL_GAME_REQUESTS:
      return action.gameRequests
    case CREATE_GAME_REQUEST:
      newState[action.requestType][action.gameRequest.id] = action.gameRequest
      return newState;
    case DELETE_GAME_REQUEST:
      delete newState[action.requestType][action.gameRequestId]
      return newState;
    default:
      return state;
  };
};
