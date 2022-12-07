import { useState, useEffect } from "react";
import {FaComments} from 'react-icons/fa';
import { useSelector } from "react-redux";
import MessagesBar from "./MessagesBar";


function MessagesButton() {
  const [display1, setDisplay1] = useState();
  const [active, setActive] = useState('');
  const view = useSelector(state => state.view);
  useEffect(() => {
    if(view !== false) {
      setDisplay1(true);
    }
  }, [view])
  useEffect(() => {
    if (display1) {
      setActive('active')
    } else {
      setActive('')
    }
  }, [display1])

  return (
    <>
      <div className={`nav-item ${active}`} onClick={() => setDisplay1(!display1)}>
        <FaComments size={25} className='nav-icon' />Messages
      </div>

      {display1 && <MessagesBar setDisplay={setDisplay1} />}
    </>
  );
}

export default MessagesButton
