//all actions specific to COMMENTS Resource
import { deleteFriendRequest } from "./friendRequests";
//imports
import { myFetch } from "./myFetch";

//constants
const GET_ALL_FRIENDS = 'friends/GET_ALL_FRIENDS';
const CREATE_FRIEND = 'friends/CREATE_FRIEND';
const DELETE_FRIEND = 'friends/DELETE_FRIEND';


//ACTION CREATORS
const getFriends = (friends) => {
  return {
    type: GET_ALL_FRIENDS,
    friends
  }
};


export const addFriend = (friend) => {
  return {
    type: CREATE_FRIEND,
    friend
  }
};


export const deleteFriend = (friendId) => {
  return {
    type: DELETE_FRIEND,
    friendId
  }
};

//Thunks

//GET ALL Comments
export const getAllFriends = () => async (dispatch) => {
  const res = await myFetch(`/api/friends`);
  if (res.ok) {
    const friends = await res.json();
    dispatch(getFriends(friends));
  }
  return res;
};

//CREATE Comment
export const acceptFriendRequest = (requestId) => async (dispatch) => {

  const res = await myFetch(`/api/friends/requests/${requestId}`, {
    method: 'PUT'
  });

  if (res.ok) {
    const newFriend = await res.json();
    dispatch(addFriend(newFriend));
    dispatch(deleteFriendRequest(requestId, 'received'))
    return res
  }
};


//DELETE Comment
export const deleteAFriend = (friendId) => async (dispatch) => {
  const res = await myFetch(`/api/friends/${friendId}`, {
    method: 'DELETE'
  });
  const response = await res.json();
  if (res.ok) {
    dispatch(deleteFriend(friendId));
  }
  return response;
};


const initialState = {};

//Comments REDUCER
export default function reducer(state = initialState, action) {
  let newState = {...state}
  switch (action.type) {
    case GET_ALL_FRIENDS:
      return action.friends
    case CREATE_FRIEND:
      newState[action.friend.id] = action.friend
      return newState;
    case DELETE_FRIEND:
      delete newState[action.friendId]
      return newState;
    default:
      return state;
  };
};
