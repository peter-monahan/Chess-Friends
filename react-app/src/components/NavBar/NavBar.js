
import React from 'react';
import { NavLink } from 'react-router-dom';
import LogoutButton from '../auth/LogoutButton';
import './NavBar.css'
const NavBar = () => {
  return (
    <nav className='nav-bar'>
      <ul>
        <li>
          <NavLink to='/' exact={true} activeClassName='active'>
            Home
          </NavLink>
        </li>
        <li>
          <NavLink to='/login' exact={true} activeClassName='active'>
            Login
          </NavLink>
        </li>
        <li>
          <NavLink to='/sign-up' exact={true} activeClassName='active'>
            Sign Up
          </NavLink>
        </li>
        <li>
          <NavLink to='/friends/requests' exact={true} activeClassName='active'>
            Friend Requests
          </NavLink>
        </li>
        <li>
          <NavLink to='/games' exact={true} activeClassName='active'>
            Games
          </NavLink>
        </li>
        <li>
          <NavLink to='/friends' exact={true} activeClassName='active'>
            Friends
          </NavLink>
        </li>
        <li>
          <NavLink to='/messages' exact={true} activeClassName='active'>
            Messages
          </NavLink>
        </li>
        <li>
          <LogoutButton />
        </li>
      </ul>
    </nav>
  );
}

export default NavBar;
