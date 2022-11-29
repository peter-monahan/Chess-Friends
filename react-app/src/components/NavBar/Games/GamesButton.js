import { useState, useEffect } from "react";
import {FaChess} from 'react-icons/fa';
import GamesBar from "./GamesBar";


function GamesButton() {
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
      <div className={`nav-item ${active}`} onClick={() => setDisplay1(!display1)}>
        <FaChess size={25} className='nav-icon' />Games
      </div>

      {display1 && <GamesBar setDisplay={setDisplay1} />}
    </>
  );
}

export default GamesButton
