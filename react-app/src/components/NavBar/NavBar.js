import { useDispatch, useSelector } from 'react-redux';
import { NavLink } from 'react-router-dom';
import {FaHome, FaComments} from 'react-icons/fa';
import LogoutButton from '../auth/LogoutButton';
import GamesButton from './Games/GamesButton'
import FriendsButton from './Friends/FriendsButton';
import MessagesButton from './Messages/MessagesButton';
import { login } from '../../store/session';

import './NavBar.css'
const NavBar = () => {
  const dispatch = useDispatch()
  const sessionUser = useSelector(state => state.session.user);
  if(!sessionUser) {
    return (
    <nav className='nav-bar'>
      <NavLink to='/' exact={true} className='nav-item' activeClassName='active'>
        <FaHome size={25} className='nav-icon' />Home
      </NavLink>
      <NavLink to='/login' exact={true} className='nav-item' activeClassName='active'>
        Login
      </NavLink>
      <NavLink to='/sign-up' exact={true} className='nav-item' activeClassName='active'>
        SignUp
      </NavLink>
      <div className='nav-item demo-users' onClick={() => dispatch(login('demo1@aa.io', 'password'))}>Demo User 1 </div>
      <div className='nav-item' onClick={() => dispatch(login('demo2@aa.io', 'password'))}>Demo User 2</div>

    </nav>
    )
  }
  return (
    <nav className='nav-bar'>
          <NavLink to='/' exact={true} className='nav-item' activeClassName='active'>
            <FaHome size={25} className='nav-icon' />Home
          </NavLink>
          <GamesButton />
          <MessagesButton />
          <FriendsButton />
          <NavLink to='/users' exact={true} className='nav-item' activeClassName='active'>
            Users
          </NavLink>
          <LogoutButton />
    </nav>
  );
}

export default NavBar;
