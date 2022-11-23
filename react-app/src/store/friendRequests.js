//all actions specific to COMMENTS Resource

//imports
import { myFetch } from "./myFetch";

//constants
const GET_ALL_FRIEND_REQUESTS = 'friendRequests/GET_ALL_FRIEND_REQUESTS';
const CREATE_FRIEND_REQUEST = 'friendRequests/CREATE_FRIEND_REQUEST';
const DELETE_FRIEND_REQUEST = 'friendRequests/DELETE_FRIEND_REQUEST';


//ACTION CREATORS
const getFriendRequests = (friendRequests) => {
  return {
    type: GET_ALL_FRIEND_REQUESTS,
    friendRequests
  }
};


export const addFriendRequest = (friendRequest, requestType) => {
  return {
    type: CREATE_FRIEND_REQUEST,
    friendRequest,
    requestType,
  }
};


const deleteFriendRequest = (friendRequestId, requestType) => {
  return {
    type: DELETE_FRIEND_REQUEST,
    friendRequestId,
    requestType,
  }
};

//Thunks

//GET ALL Comments
export const getAllFriendRequests = () => async (dispatch) => {
  const res = await myFetch(`/api/friends/requests`);
  if (res.ok) {
    const friendRequests = await res.json();
    dispatch(getFriendRequests(friendRequests));
  }
  return res;
};

//CREATE Comment
export const createFriendRequest = (receiver_id) => async (dispatch) => {

  const res = await myFetch(`/api/friends/requests`, {
    method: 'POST',
    body: JSON.stringify({
      receiver_id
    })
  });

  if (res.ok) {
    const newFriendRequest = await res.json();
    dispatch(addFriendRequest(newFriendRequest, 'sent'));
    return res
  }
};


//DELETE Comment
export const deleteAFriendRequest = (friendRequestId) => async (dispatch) => {
  const res = await myFetch(`/api/friends/requests/${friendRequestId}`, {
    method: 'DELETE'
  });
  const response = await res.json();
  if (res.ok) {
    dispatch(deleteFriendRequest(friendRequestId, response.requestType));
  }
  return response;
};


const initialState = {sent: {}, received: {}};

//Comments REDUCER
export default function reducer(state = initialState, action) {
  let newState = {sent:{...state.sent}, received: {...state.received}}
  switch (action.type) {
    case GET_ALL_FRIEND_REQUESTS:
      return action.friendRequests
    case CREATE_FRIEND_REQUEST:
      newState[action.requestType][action.friendRequest.id] = action.friendRequest
      return newState;
    case DELETE_FRIEND_REQUEST:
      delete newState[action.requestType][action.friendRequestId]
      return newState;
    default:
      return state;
  };
};
