//all actions specific to COMMENTS Resource
//imports
import { myFetch } from "./myFetch";

//constants
const GET_ALL_USERS = 'users/GET_ALL_USERS';
const CREATE_USER = 'users/CREATE_USER';
// const DELETE_USER = 'users/DELETE_USER';


//ACTION CREATORS
const getUsers = (users) => {
  return {
    type: GET_ALL_USERS,
    users
  }
};


const addUser = (user) => {
  return {
    type: CREATE_USER,
    user
  }
};


// const deleteUser = (userId) => {
//   return {
//     type: DELETE_USER,
//     userId
//   }
// };

//Thunks

//GET ALL Comments
export const getAllUsers = () => async (dispatch) => {
  const res = await myFetch(`/api/users`);
  if (res.ok) {
    const users = await res.json();
    dispatch(getUsers(users));
  }
  return res;
};

export const getAUser = (id) => async (dispatch) => {
  const res = await myFetch(`/api/users/${id}`);
  if (res.ok) {
    const user = await res.json();
    dispatch(addUser(user));
  }
  return res;
};



const initialState = {};

//Comments REDUCER
export default function reducer(state = initialState, action) {
  let newState = {...state}
  switch (action.type) {
    case GET_ALL_USERS:
      return action.users
    case CREATE_USER:
      newState[action.user.id] = action.user
      return newState;
    // case DELETE_USER:
    //   delete newState[action.userId]
    //   return newState;
    default:
      return state;
  };
};
