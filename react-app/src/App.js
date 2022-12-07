import React, { useState, useEffect } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
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
import {addFriend} from './store/friends';
import {deleteFriendRequest} from './store/friendRequests';
import {addGame} from './store/games';
import {deleteGameRequest, addGameRequest} from './store/gameRequests';

let socket;

function App() {
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

      socket.on("connect", () => {
        console.log('Connected')
      });
      socket.on("disconnect", () => {
        console.log('Disconnected')
      });
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
      });
      socket.on('new_game', ({game, requestId}) => {
        dispatch(addGame(game));
        dispatch(deleteGameRequest(requestId, 'sent'))
      });
      socket.on('update_game', (game) => {
        dispatch(addGame(game));
      });
      socket.on('new_game_request', ({gameRequest, requestType}) => {
        dispatch(addGameRequest(gameRequest, requestType));
      });
      socket.onAny((message, ...args) => {
        console.log(message, args)
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
    <BrowserRouter>
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
    </BrowserRouter>
  );
}

export default App;
