import { useState, useEffect } from "react";
import { useDispatch, useSelector } from 'react-redux';
import {FaUserFriends} from 'react-icons/fa';
import FriendsBar from "./FriendsBar";


function FriendsButton() {
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
        <FaUserFriends size={25} className='nav-icon' />Friends
      </div>

      {display1 && <FriendsBar setDisplay={setDisplay1} />}
    </>
  );
}

export default FriendsButton
