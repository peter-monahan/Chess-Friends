import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getAUser } from '../../store/users';
import { useParams } from 'react-router-dom';
import {createFriendRequest} from '../../store/friendRequests';
import {createGameRequest} from '../../store/gameRequests';
import {createChat} from '../../store/chats';
import {setView} from '../../store/view';
import './User.css'
function User() {
  const dispatch = useDispatch()
  const { userId }  = useParams();
  const user = useSelector(state => state.users[userId]);
  const sessionUser = useSelector(state => state.session.user);

  useEffect(() => {
    dispatch(getAUser(userId))
  }, [userId]);

  if (!user) {
    return null;
  }

  const buttons = (
    <div>
      { !user.is_friend && <button onClick={() => dispatch(createFriendRequest(userId))}>Send Friend Request</button>}
      <button onClick={() => dispatch(createGameRequest(userId))}>Send Game Invite</button>
      <button onClick={() => {dispatch(createChat(userId)); dispatch(setView(Number(userId)))}}>Send Direct Message</button>
   </div>
  )

  return (
    <div className='user-page-div'>
      <div className='user-page-top'>
        <img src={user?.profile_image_url || '/images/white,pawn.png'} className="user-page-img"></img>
        <div>{user?.username}<div className={`active-${user?.active}`}></div></div>
      </div>

      {sessionUser && user.id !== sessionUser.id && buttons}

    </div>
  );
}
export default User;
