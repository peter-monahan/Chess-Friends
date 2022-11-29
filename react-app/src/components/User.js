import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getAUser } from '../store/users';
import { useParams } from 'react-router-dom';
import {createFriendRequest} from '../store/friendRequests';
import {createGameRequest} from '../store/gameRequests';
import {createChat} from '../store/chats';

function User() {
  const dispatch = useDispatch()
  const { userId }  = useParams();
  const user = useSelector(state => state.users[userId]);

  useEffect(() => {
    dispatch(getAUser(userId))
  }, [userId]);

  if (!user) {
    return null;
  }

  return (
    <ul>
      <li>
        <strong>User Id</strong> {userId}
      </li>
      <li>
        <strong>Username</strong> {user?.username}
      </li>
      <li>
        <button onClick={() => dispatch(createFriendRequest(userId))}>Create Friend Request</button>
      </li>
      <li>
        <button onClick={() => dispatch(createGameRequest(userId))}>Create Game Request</button>
      </li>
      <li>
        <button onClick={() => dispatch(createChat(userId))}>Create Chat</button>
      </li>
    </ul>
  );
}
export default User;
