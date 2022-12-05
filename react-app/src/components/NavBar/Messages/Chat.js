import { useState, useEffect, useRef } from "react";
import { useDispatch, useSelector } from 'react-redux';
import { createMessage, deleteAMessage, getAllMessages, editMessage } from '../../../store/messages';
import { Link } from "react-router-dom";
import Message from "./Message";
import './Chat.css';

function Chat({setDisplay, chat}) {
  const divRef = useRef(null)
  const dispatch = useDispatch();
  const messages = useSelector(state => state.messages)
  const sessionUser = useSelector(state => state.session.user);
  const [newMessage, setNewMessage] = useState('');
  const [errors, setErrors] = useState([]);
  const otherUser = chat.user

  function handleClick(e) {
    const targ = e.target;
    if(!(targ.id.includes('chat-bar'))){
      setDisplay(false);
    }
  }
  useEffect(() => {
    document.addEventListener('click', handleClick);
    const  func = async () => {
      await dispatch(getAllMessages(otherUser.id))
      divRef.current?.scrollIntoView()
    }
    divRef.current?.scrollIntoView()
    func()
    return () => {
      document.removeEventListener('click', handleClick)
    }
  }, [])
  useEffect(() => {
    divRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])


  useEffect(() => {
    const tempArr = []
    if(newMessage.length > 0) {
      if(newMessage.split(' ').join('\n').split('\n').length === newMessage.length+1) {
        tempArr.push('Must contain at least one character')
      }
    }
    setErrors(tempArr)
  }, [newMessage]);
//   const Message = ({message}) => {
//     let owned;
//     if(message.sender_id === sessionUser.id) {
//       owned = true;
//     } else {

//       owned = false;
//     }
//     return (
//     <div className={`chat-message-${side}`} id="message-bar-chat-bar">
//       <div id="message-bar-chat-bar" className="message">
//         <div id="message-bar-chat-bar">{user.username}</div>
//         <div id="message-bar-chat-bar">{message.content}</div>
//         {owned && <button id="message-bar-chat-bar">Edit</button>}
//       </div>
//     </div>
//   )
// }

const createNewMessage = (e) => {
  e.preventDefault();

  const payload = {
    content: newMessage
  }
  if(errors.length) {
    setNewMessage('');
  } else {
    dispatch(createMessage(payload, otherUser.id));
    setNewMessage('');
  }
}

  const Messages = () => (
    <>
      {Object.keys(messages[otherUser.id]).map(key => {
        const message = messages[otherUser.id][key];
        let owned;
        if(message.sender_id === sessionUser.id) {
          owned = true;
        } else {
          owned = false;
        }
        return (
            <Message key={key} owned={owned} message={message} />
        )
      })}
    </>
  )

  const ResponseBox = (
      <div id="message-bar-chat-bar" className="response-box">
        <textarea maxLength='200' rows={newMessage.split(' ').join('').split('\n').reduce((acc, curr) => {
            if(acc >= 6) {
              return 6;
            }
            if(curr.length === 0 ) {
              return acc + 1
            }
            return acc + Math.ceil(curr.length / 40)
            }, 1) } cols='40'
        placeholder='Send a message' className="message-textarea"
        value={newMessage} onChange={e => setNewMessage(e.target.value)}
        id="message-bar-chat-bar">
        </textarea>
        <button id="message-bar-chat-bar" className="send-button" onClick={createNewMessage} disabled={newMessage.length <= 0}>Send</button>
      </div>
    )


  return (
    <div className="chat-bar" id="message-bar-chat-bar">
      <div id="message-bar-chat-bar" className="messages-container">
        <div className="messages" id="message-bar-chat-bar">
          {messages[otherUser.id] !== undefined && <Messages />}
          <div ref={divRef} className="dummy-div"></div>
        </div>
      </div>
      {ResponseBox}
    </div>
  );
}

export default Chat
