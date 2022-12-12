import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getAllUsers } from '../../store/users';
import { NavLink } from 'react-router-dom';

import './User.css'

function UsersList() {
  const dispatch = useDispatch()
  const users = useSelector(state => state.users);

  useEffect(() => {
    dispatch(getAllUsers())
  }, []);

  const userComponents = Object.keys(users).map((key) => {
    const user = users[key]
    return (
        <NavLink key={user.id} className='list-user' to={`/users/${user.id}`}>{user.username}</NavLink>
    );
  });

  return (
    <>
      <h1>User List</h1>
      <div className='user-list'>{userComponents}</div>
    </>
  );
}

export default UsersList;
