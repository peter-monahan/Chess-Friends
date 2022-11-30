import { useState, useEffect } from "react";
import { createMessage, deleteAMessage, getAllMessages, editMessage } from '../../../store/messages';

function Message({owned, message}) {
  let side;
  if(owned) {
    side = 'right';
  } else {
    side = 'left';
  }

  return (
    <div className={`chat-message-${side}`} id="message-bar-chat-bar">
      <div id="message-bar-chat-bar" className="message">
        {/* <div id="message-bar-chat-bar">{user.username}</div> */}
        <div id="message-bar-chat-bar">{message.content}</div>
        {owned && <button id="message-bar-chat-bar">Edit</button>}
      </div>
    </div>
  )
}

export default Message
