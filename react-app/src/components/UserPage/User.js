import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getAUser } from '../../store/users';
import { useParams, useHistory } from 'react-router-dom';
import {createFriendRequest, deleteAFriendRequest} from '../../store/friendRequests';
import {createGameRequest, deleteAGameRequest} from '../../store/gameRequests';
import {createChat} from '../../store/chats';
import {setView} from '../../store/view';
import './User.css'
import { acceptFriendRequest, deleteAFriend } from '../../store/friends';
import { acceptGameRequest } from '../../store/games';
function User() {
  const history = useHistory()
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
      <div>
      {(user.is_friend !== undefined && !user.is_friend && !user.sent_to_friend_req && !user.received_from_friend_req && <button onClick={() => dispatch(createFriendRequest(userId)).then(() => dispatch(getAUser(userId)))}>Send Friend Request</button>) ||
      <div>
        {user.is_friend !== undefined && !user.is_friend && user.received_from_friend_req && <button onClick={() => dispatch(acceptFriendRequest(user.received_from_friend_req.id)).then(() => dispatch(getAUser(userId)))}>Accept Friend Request</button>}
        {user.is_friend !== undefined && !user.is_friend && (user.sent_to_friend_req || user.received_from_friend_req) && <button onClick={() => dispatch(deleteAFriendRequest(user.sent_to_friend_req ? user.sent_to_friend_req.id : user.received_from_friend_req.id)).then(() => dispatch(getAUser(userId)))}>Delete Friend Request</button>}
      </div>
      }
      </div>
      <div>
      {(user.is_friend !== undefined && !user.sent_to_game_req && !user.received_from_game_req && <button onClick={() => dispatch(createGameRequest(userId)).then(() => dispatch(getAUser(userId)))}>Send Game Invite</button>) ||
      <div>

        {user.is_friend !== undefined &&  user.received_from_game_req && <button onClick={() => dispatch(acceptGameRequest(user.received_from_game_req.id)).then((id) => history.replace(`/games/${id}`))}>Accept Game Invite</button>}
        {user.is_friend !== undefined &&  (user.sent_to_game_req || user.received_from_game_req) && <button onClick={() => dispatch(deleteAGameRequest(user.sent_to_game_req ? user.sent_to_game_req.id : user.received_from_game_req.id)).then(() => dispatch(getAUser(userId)))}>Delete Game Invite</button>}
      </div>
      }
      </div>
      <div>
        <button onClick={() => {dispatch(createChat(userId)); dispatch(setView(Number(userId)))}}>Send Direct Message</button>
      </div>
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
