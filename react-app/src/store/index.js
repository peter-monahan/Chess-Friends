import { createStore, combineReducers, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';
import session from './session'
import chats from './chats';
import messages from './messages';
import friends from './friends';
import friendRequests from './friendRequests';
import games from './games';
import gameRequests from './gameRequests';
import users from './users';


const rootReducer = combineReducers({
  session,
  games,
  gameRequests,
  messages,
  chats,
  friends,
  friendRequests,
  users,
});


let enhancer;

if (process.env.NODE_ENV === 'production') {
  enhancer = applyMiddleware(thunk);
} else {
  const logger = require('redux-logger').default;
  const composeEnhancers =
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
  enhancer = composeEnhancers(applyMiddleware(thunk, logger));
}

const configureStore = (preloadedState) => {
  return createStore(rootReducer, preloadedState, enhancer);
};

export default configureStore;
