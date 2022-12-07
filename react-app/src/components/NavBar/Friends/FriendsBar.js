import { useState, useEffect } from "react";
import { useDispatch, useSelector } from 'react-redux';
import { Link } from "react-router-dom";
import {getAllFriendRequests, deleteAFriendRequest} from '../../../store/friendRequests'
import {getAllFriends, acceptFriendRequest} from '../../../store/friends';
import './FriendsBar.css';

function FriendsBar({setDisplay}) {
  const dispatch = useDispatch()
  const [requestsType, setRequestsType] = useState('received');
  const friendRequests = useSelector(state => state.friendRequests);
  const friends = useSelector(state => state.friends);


  function handleClick(e) {
    const targ = e.target;
    if(!(targ.id === 'friend-bar')){
      setDisplay(false);
    }
  }

  useEffect(() => {
    document.addEventListener('click', handleClick);
    dispatch(getAllFriends())
    dispatch(getAllFriendRequests())

    return () => {
      document.removeEventListener('click', handleClick)
    }
  }, [])

  const ReceivedRequests = () => (
    <>
      {Object.keys(friendRequests.received).map(key => {
        const request = friendRequests.received[key];
        return (
          <div key={key} id='friend-bar' className="friend-request">
            {request.sender.username}
            <div id='friend-bar'>

            <button onClick={() => dispatch(acceptFriendRequest(request.id))} id="friend-bar">Accept</button>
            <button onClick={() => dispatch(deleteAFriendRequest(request.id))} id="friend-bar">Decline</button>
            </div>
          </div>
        )
      })}
    </>
  )

  const SentRequests = () => (
    <>
      {Object.keys(friendRequests.sent).map(key => {
        const request = friendRequests.sent[key];
        return (
          <div key={key} id='friend-bar' className="friend-request">
            {request.receiver.username}
            <button onClick={() => dispatch(deleteAFriendRequest(request.id))} id='friend-bar'>Delete</button>
          </div>
        )
      })}
    </>
  )

  const Friends = () => (
    <>
      {Object.keys(friends).map(key => {
        const friend = friends[key];

        return (
          <Link className="friend-button" to={`/users/${friend.id}`} key={key}>
            {friend.username}<div className={`active-${friend.active}`}></div>
          </Link>
        )
      })}
    </>
  )

  return (
    <div className="friend-bar" id="friend-bar">
      <div id='friend-bar' className="friend-requests">
        Friend Requests
        <div className="friend-sent-received" id="friend-bar">
          <div onClick={(e) => setRequestsType('received')} className={`friend-received friend-tab ${requestsType === 'received' ? 'active' : ''}`} id="friend-bar">Received</div>
          <div onClick={(e) => setRequestsType('sent')} className={`friend-sent friend-tab ${requestsType === 'sent' ? 'active' : ''}`} id="friend-bar">Sent</div>
        </div>
        <div className="friend-requests-info" id="friend-bar">
          {requestsType === 'received' ? <ReceivedRequests /> : <SentRequests />}
        </div>
      </div>
      <div id='friend-bar' className="friends">
        Friends
        <div className="friends-info" id="friend-bar">
          <Friends />
        </div>
      </div>
    </div>
  );
}

export default FriendsBar
