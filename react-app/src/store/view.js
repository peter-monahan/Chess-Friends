

//constants

const SET_VIEW = 'view/SET_VIEW';
const DELETE_VIEW = 'view/DELETE_VIEW';


//ACTION CREATORS
export const setView = (id) => {
  return {
    type: SET_VIEW,
    id,
  }
};


export const deleteView = () => {
  return {
    type: DELETE_VIEW,
  }
};


const initialState = false;

//Comments REDUCER
export default function reducer(state = initialState, action) {
  switch (action.type) {
    case SET_VIEW:
      return action.id
    case DELETE_VIEW:
      return false;
    default:
      return state;
  };
};
