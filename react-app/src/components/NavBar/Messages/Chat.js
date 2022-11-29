import { useState, useEffect } from "react";
import { useDispatch, useSelector } from 'react-redux';
import { createMessage, deleteAMessage, getAllMessages, editMessage } from '../../../store/messages';
import { Link } from "react-router-dom";
import './Chat.css';

function Chat({setDisplay, chat}) {
  const dispatch = useDispatch();
  const messages = useSelector(state => state.messages)
  const sessionUser = useSelector(state => state.session.user);
  const [newMessage, setNewMessage] = useState('');
  const otherUser = chat.user

  function handleClick(e) {
    const targ = e.target;
    if(!(targ.id.includes('chat-bar'))){
      setDisplay(false);
    }
  }

  useEffect(() => {
    document.addEventListener('click', handleClick);
    dispatch(getAllMessages(otherUser.id))


    return () => {
      document.removeEventListener('click', handleClick)
    }
  }, [])

  const Message = ({message}) => {
    let side;
    let user;
    let owned;
    if(message.sender_id === sessionUser.id) {
      side = 'right';
      user = sessionUser;
      owned = true;
    } else {
      side = 'left';
      user = otherUser;
      owned = false;
    }
    return (
    <div className={`chat-message-${side}`} id="message-bar-chat-bar">
      <div id="message-bar-chat-bar" className="message">
        <div id="message-bar-chat-bar">{user.username}</div>
        <div id="message-bar-chat-bar">{message.content}</div>
      </div>
    </div>
  )
}
  const Messages = () => (
    <>
      {Object.keys(messages[otherUser.id]).map(key => {
        const message = messages[otherUser.id][key];

        return (
            <Message key={key} message={message} />
        )
      })}
    </>
  )

  const ResponseBox = () => {

    return (
      <div id="message-bar-chat-bar" className="response-box">
        <textarea maxLength='200' rows='5' cols='50'
        placeholder='Send a message' className="comment-textarea"
        value={newMessage} onChange={e => setNewMessage(e.target.value)}
        id="message-bar-chat-bar">
        </textarea>
      </div>
    )
  }

  return (
    <div className="chat-bar" id="message-bar-chat-bar">
      <div className="messages" id="message-bar-chat-bar">
        {messages[otherUser.id] !== undefined && <Messages />}
      </div>
      <ResponseBox />
    </div>
  );
}

export default Chat
