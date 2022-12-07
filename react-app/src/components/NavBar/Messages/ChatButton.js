import { useState, useEffect} from "react";
import { useDispatch, useSelector } from "react-redux";
import { deleteView } from "../../../store/view";

import Chat from "./Chat";


function ChatButton({chat, userId}) {
  const dispatch = useDispatch()
  const [display1, setDisplay1] = useState(false);
  const [active, setActive] = useState('');
  const view = useSelector(state => state.view)
  useEffect(() => {
    if (display1) {
      setActive('active')
    } else {
      setActive('')
    }
  }, [display1])

  useEffect(() => {
    if(chat.user.id === view) {
      setDisplay1(true)
      // dispatch(deleteView())
    }

  }, [view])


  return (
    <>
      <div id="message-bar" className={`chat-button ${active}`} onClick={() => setDisplay1(!display1)}>
        <div id="message-bar">{chat.user.username}<div id="message-bar" className={`active-${chat.user.active}`}></div></div>
        { chat.message !== null && <div id="message-bar" className="recent-message">{chat.message.sender_id === userId ? 'You: ' : ''}{chat.message.content}</div>}
      </div>

      {display1 && <Chat setDisplay={setDisplay1} chat={chat} />}
    </>
  );
}

export default ChatButton
