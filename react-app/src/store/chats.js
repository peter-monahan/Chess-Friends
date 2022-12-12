//all actions specific to COMMENTS Resource

//imports
import { myFetch } from "./myFetch";

//constants
const GET_ALL_CHATS = 'chats/GET_ALL_CHATS';
const CREATE_CHAT = 'chats/CREATE_CHAT';
const DELETE_CHAT = 'chats/DELETE_CHAT';


//ACTION CREATORS
const getChats = (chats) => {
  return {
    type: GET_ALL_CHATS,
    chats
  }
};


export const addChat = (chat) => {
  return {
    type: CREATE_CHAT,
    chat,
  }
};


const deleteChat = (chatId) => {
  return {
    type: DELETE_CHAT,
    chatId
  }
};

//Thunks

//GET ALL Comments
export const getAllChats = () => async (dispatch) => {
  const res = await myFetch(`/api/messages/views`);
  if (res.ok) {
    const chats = await res.json();
    dispatch(getChats(chats));
    return chats
  }

};

//CREATE Comment
export const createChat = (userId) => async (dispatch) => {

  const res = await myFetch(`/api/messages/views/with/${userId}`, {
    method: 'POST',
  });

  if (res.ok) {
    const newChat = await res.json();
    dispatch(addChat(newChat));
    return res
  }
};


//DELETE Comment
export const deleteAChat = (chatId) => async (dispatch) => {
  const res = await myFetch(`/api/messages/views/${chatId}`, {
    method: 'DELETE'
  });
  const response = await res.json();
  if (res.ok) {
    dispatch(deleteChat(chatId));
  }
  return response;
};


const initialState = {};

//Comments REDUCER
export default function reducer(state = initialState, action) {
  let newState = { ...state }
  switch (action.type) {
    case GET_ALL_CHATS:
      return action.chats
    case CREATE_CHAT:
      newState[action.chat.id] = action.chat
      return newState;
    case DELETE_CHAT:
      delete newState[action.chatId]
      return newState;
    default:
      return state;
  };
};
