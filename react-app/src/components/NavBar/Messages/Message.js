import { useState, useEffect } from "react";
import { createMessage, deleteAMessage, getAllMessages, editMessage } from '../../../store/messages';
import { useDispatch } from "react-redux";

function Message({owned, message}) {
  const dispatch = useDispatch();
  const [showEdit, setShowEdit] = useState(false);
  const [display1, setDisplay1] = useState(false);

  const [newMessage, setNewMessage] = useState(message.content);
  const [errors, setErrors] = useState([]);

  const sentDate = new Date(message.created_at)
  const now = new Date()

  function handleClick(e) {
    setDisplay1(false);
  }

  useEffect(() => {
    if(display1) {
      document.addEventListener('click', handleClick);

      return () => {
        document.removeEventListener('click', handleClick)
      }
    }

  }, [display1])

  const saveMessage = (e) => {
    e.preventDefault();


    const payload = {
      content: newMessage
    }
    if(errors.length) {
      dispatch(deleteAMessage(message.id))
      setNewMessage('');
    } else {
      dispatch(editMessage(payload, message.id));
      setNewMessage('');
    }
  }
  const destroyMessage = (e) => {
    e.preventDefault();
    dispatch(deleteAMessage(message.id))
    setNewMessage('');
  }

  useEffect(() => {
    const tempArr = []
    if(newMessage.length > 0) {
      if(newMessage.split(' ').join('\n').split('\n').length === newMessage.length+1) {
        tempArr.push('Must contain at least one character')
      }
    } else {
      tempArr.push('Must contain at least one character');
    }
    setErrors(tempArr)
  }, [newMessage]);

  let side;
  if(owned) {
    side = 'right';
  } else {
    side = 'left';
  }

if(showEdit) {
  return (
    <div className={`chat-message-${side}`} id="message-bar-chat-bar">
      <div id="message-bar-chat-bar" className="message">
        <div className="comment-body edit-area" id="message-bar-chat-bar">
          {/* {displayErrors && errors.length > 0 ? errorsBox: null} */}
          <textarea id="message-bar-chat-bar" maxLength='200' cols='20' rows={newMessage.split(' ').join('').split('\n').reduce((acc, curr) => {
            return acc + Math.ceil(curr.length / 22)
            }, 1) } value={newMessage} onChange={e => setNewMessage(e.target.value)} className='message-textarea'></textarea>
          <button id="message-bar-chat-bar" onClick={saveMessage} className='publish-btn'>Save</button>
          {/* <button id="message-bar-chat-bar" onClick={destroyMessage} className='cancel-btn-updatepage'>Delete</button> */}
        </div>
      </div>
    </div>
  )
}

  return (
    <div className={`chat-message-${side}`} id="message-bar-chat-bar">
      <div id="message-bar-chat-bar" className="message">
        <div id="message-bar-chat-bar" className="message-mid">
          <div className="message-body" id="message-bar-chat-bar">{message.content}</div>
          {owned && <div className="message-settings-button" id="message-bar-chat-bar" onClick={() => setDisplay1(!display1)}>⋮</div>}
          {display1 && <div id="message-bar-chat-bar"><button id="message-bar-chat-bar" onClick={() => setShowEdit(true)}>Edit</button><button id="message-bar-chat-bar" onClick={destroyMessage}>Delete</button></div>}
        </div>

        {message.created_at !== message.updated_at && <div id="message-bar-chat-bar" className="edited-text">edited</div>}
        <div id="message-bar-chat-bar" className="datetime-text">{`${sentDate.toDateString()}, ${sentDate.toLocaleTimeString()}`}</div>
      </div>
    </div>
  )
}

export default Message
