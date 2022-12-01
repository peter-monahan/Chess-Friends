import { useState, useEffect } from "react";
import { useDispatch, useSelector } from 'react-redux';
import { Link } from "react-router-dom";
import { getAllChats } from '../../../store/chats';
import ChatButton from './ChatButton';
import './MessagesBar.css';

function MessagesBar({setDisplay}) {
  const dispatch = useDispatch()
  const chats = useSelector(state => state.chats);
  const sessionUser = useSelector(state => state.session.user);

  function handleClick(e) {
    const targ = e.target;
    if(!(targ.id.includes('message-bar'))){
      setDisplay(false);
    }
  }

  useEffect(() => {
    document.addEventListener('click', handleClick);
    dispatch(getAllChats())

    return () => {
      document.removeEventListener('click', handleClick)
    }
  }, [])


  const Chats = () => (
    <>
      {Object.keys(chats).map(key => {
        const chat = chats[key];

        return (
            <ChatButton chat={chat} userId={sessionUser.id} />
        )
      })}
    </>
  )

  return (
    <div className="message-bar" id="message-bar">
    <Chats />
    </div>
  );
}

export default MessagesBar
