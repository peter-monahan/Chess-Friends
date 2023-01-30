import React, { useState, useEffect } from 'react';
import {Route, Switch, useHistory } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import LoginForm from './components/auth/LoginForm';
import SignUpForm from './components/auth/SignUpForm';
import NavBar from './components/NavBar/NavBar';
import ProtectedRoute from './components/auth/ProtectedRoute';
import UsersList from './components/UserPage/UsersList';
import User from './components/UserPage/User';
import Game from './components/Game/Game';
import Splash from './components/Splash/Splash';
import { authenticate } from './store/session';
import { io } from 'socket.io-client';
import {addChat} from './store/chats';
import {addMessage, deleteMessage} from './store/messages';
import {addFriend, deleteFriend} from './store/friends';
import {addFriendRequest, deleteFriendRequest} from './store/friendRequests';
import {addGame} from './store/games';
import {deleteGameRequest, addGameRequest} from './store/gameRequests';
import { getAUser } from './store/users';

let socket;

function App() {
  const history = useHistory()
  const [loaded, setLoaded] = useState(false);
  const [view, setView] = useState(false);
  const dispatch = useDispatch();
  const user = useSelector(state => state.session.user)
  useEffect(() => {
    (async() => {
      await dispatch(authenticate());
      setLoaded(true);
    })();
  }, [dispatch]);

  useEffect(() => {
    if(user) {
      socket = io()

      // socket.on("connect", () => {
      //   console.log('Connected')
      // });
      // socket.on("disconnect", () => {
      //   console.log('Disconnected')
      // });
      socket.on('new_chat', (chat) => {
        dispatch(addChat(chat))
      });
      socket.on('new_message', (message) => {
        dispatch(addMessage(message, message.sender_id))
      });
      socket.on('delete_message', (message) => {
        dispatch(deleteMessage(message.id, message.sender_id))
      });
      socket.on('edit_message', (message) => {
        dispatch(addMessage(message, message.sender_id))
      });
      socket.on('new_friend', ({friend, requestId}) => {
        dispatch(addFriend(friend));
        dispatch(deleteFriendRequest(requestId, 'sent'))
        dispatch(getAUser(friend.id))
      });
      socket.on('delete_friend', (friend) => {
        dispatch(deleteFriend(friend.id));
        dispatch(getAUser(friend.id))
      });
      socket.on('new_game', ({game, requestId}) => {
        dispatch(addGame(game));
        if (requestId) {
          dispatch(deleteGameRequest(requestId, 'sent'))
          dispatch(getAUser(game.black_id))
        } else {
          history.replace(`/games/${game.id}`);
        }

      });
      socket.on('update_game', (game) => {
        dispatch(addGame(game));
      });
      socket.on('new_game_request', ({gameRequest, requestType}) => {
        dispatch(addGameRequest(gameRequest, requestType));
        dispatch(getAUser(gameRequest.user_id))
      });
      socket.on('new_friend_request', ({friendRequest, requestType}) => {
        dispatch(addFriendRequest(friendRequest, requestType));
        dispatch(getAUser(friendRequest.sender_id))

      });
      socket.on('delete_friend_request', ({request, requestType}) => {
        dispatch(deleteFriendRequest(request.id, requestType));
        if(requestType === 'sent'){
          dispatch(getAUser(request.receiver_id))
        } else if(requestType === 'received'){
          dispatch(getAUser(request.sender_id))
        }
      })
      socket.on('delete_game_request', ({request, requestType}) => {
        dispatch(deleteGameRequest(request.id, requestType));
        if(requestType === 'sent'){
          dispatch(getAUser(request.opponent_id))
        } else if(requestType === 'received'){
          dispatch(getAUser(request.user_id))
        }
      })
      socket.onAny((message, ...args) => {
        console.log(message, ...args)
      })
    } else if(socket) {
      socket.disconnect()
    }
  //   return (() => {
  //     socket.disconnect()
  // })
  }, [user])


  if (!loaded) {
    return null;
  }

  return (
    <div className='main-container'>

      <NavBar view={view} setView={setView} />
      <Switch>
        <Route path='/login' exact={true}>
          <LoginForm />
        </Route>
        <Route path='/sign-up' exact={true}>
          <SignUpForm />
        </Route>
        <Route path='/users' exact={true} >
          <UsersList/>
        </Route>

        <Route path='/users/:userId' exact={true} >
          <User setView={setView} />
        </Route>
        <ProtectedRoute path='/games/:gameId' exact={true} >
          <Game />
        </ProtectedRoute>
        <Route path='/' exact={true} >
          <Splash />
        </Route>

      </Switch>
    </div>
  );
}

export default App;
