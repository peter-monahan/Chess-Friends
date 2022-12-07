import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getAllUsers } from '../../store/users';
import { NavLink } from 'react-router-dom';

function UsersList() {
  const dispatch = useDispatch()
  const users = useSelector(state => state.users);

  useEffect(() => {
    dispatch(getAllUsers())
  }, []);

  const userComponents = Object.keys(users).map((key) => {
    const user = users[key]
    return (
      <li key={user.id}>
        <NavLink to={`/users/${user.id}`}>{user.username}</NavLink>
      </li>
    );
  });

  return (
    <>
      <h1>User List: </h1>
      <ul>{userComponents}</ul>
    </>
  );
}

export default UsersList;
