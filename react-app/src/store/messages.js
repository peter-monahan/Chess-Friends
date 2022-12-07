//all actions specific to MESSAGES Resource

//imports
import { myFetch } from "./myFetch";

//constants
const GET_MESSAGES = 'messages/GET_MESSAGES';
const ADD_MESSAGE = 'messages/ADD_MESSAGE';
const DELETE_MESSAGE = 'messages/DELETE_MESSAGE';


//ACTION CREATORS
const getMessages = (messages, userId) => {
  return {
    type: GET_MESSAGES,
    messages,
    userId
  }
};


export const addMessage = (message, userId) => {
  return {
    type: ADD_MESSAGE,
    message,
    userId
  }
};


export const deleteMessage = (messageId, userId) => {
  return {
    type: DELETE_MESSAGE,
    messageId,
    userId
  }
};

//Thunks

//GET ALL Messages
export const getAllMessages = (userId) => async (dispatch) => {
  const res = await myFetch(`/api/messages/with/${userId}`);
  if (res.ok) {
    const messages = await res.json();
    dispatch(getMessages(messages, userId));
  }
  return res;
};


//SINGLE MESSAGE
export const getMessage = (messageId) => async (dispatch) => {
  const res = await myFetch(`/api/messages/${messageId}`)

  if (res.ok) {
    const message = await res.json();
    dispatch(addMessage(message, message?.receiver_id))
  };
};

//CREATE Message
export const createMessage = (message, userId) => async (dispatch) => {
  const { content } = message;

  const res = await myFetch(`/api/messages/with/${userId}`, {
    method: 'POST',
    body: JSON.stringify({
      content
    })
  });

  if (res.ok) {
    const newMessage = await res.json();
    dispatch(addMessage(newMessage, userId));
    return res
  }
};


//UPDATE Message
export const editMessage = (message, messageId) => async (dispatch) => {
  const { content } = message;
  const res = await myFetch(`/api/messages/${messageId}`, {
    method: 'PUT',
    body: JSON.stringify({
      content
    }),
  });

  if (res.ok) {
    const updatedMessage = await res.json();
    dispatch(addMessage(updatedMessage, updatedMessage?.receiver_id));
    return res
  }
};


//DELETE Message
export const deleteAMessage = (messageId) => async (dispatch) => {
  const res = await myFetch(`/api/messages/${messageId}`, {
    method: 'DELETE'
  });
  const response = await res.json();
  if (res.ok) {
    dispatch(deleteMessage(messageId, response.item.receiver_id));
  }
  return response;
};


const initialState = {};

//Messages REDUCER
export default function reducer(state = initialState, action) {
  let newState = { ...state }
  newState[action.userId] = state[action.userId]
  switch (action.type) {
    case GET_MESSAGES:
      newState[action.userId] = action.messages
      return newState
    case ADD_MESSAGE:
      if(newState[action.userId]) {
        newState[action.userId][action.message.id] = action.message;
      } else {
        newState[action.userId] = {};
        newState[action.userId][action.message.id] = action.message;
      }
      return newState;
    case DELETE_MESSAGE:
      delete newState[action.userId][action.messageId]
      return newState;
    default:
      return state;
  };
};
