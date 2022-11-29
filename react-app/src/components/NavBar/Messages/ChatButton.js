import { useState, useEffect } from "react";

import Chat from "./Chat";


function ChatButton({chat}) {
  const [display1, setDisplay1] = useState(false);
  const [active, setActive] = useState('');

  useEffect(() => {
    if (display1) {
      setActive('active')
    } else {
      setActive('')
    }
  }, [display1])

  return (
    <>
      <div id="message-bar" className={`chat-button ${active}`} onClick={() => setDisplay1(!display1)}>
        {chat.user.username}
      </div>

      {display1 && <Chat setDisplay={setDisplay1} chat={chat} />}
    </>
  );
}

export default ChatButton
