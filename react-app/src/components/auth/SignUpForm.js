import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux'
import { Redirect } from 'react-router-dom';
import { signUp } from '../../store/session';
import './auth.css'

const SignUpForm = () => {
  const [errors, setErrors] = useState([]);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [repeatPassword, setRepeatPassword] = useState('');
  const [hasSubmitted, setHasSubmitted] = useState(false);

  const user = useSelector(state => state.session.user);
  const dispatch = useDispatch();

  const validEmail = (email) => {
    const split = email.split('@');

    if(split.length > 1 && split[0].length && split[1].length) {
      const end = split[1].split('.');
      if(end.length > 1 && end[0].length && end[1].length) {
        return true;
      }
    }
    return false
  }

  useEffect(() => {
    const errors = [];
    if(!validEmail(email)) errors.push('Please provide a valid email');
    if(username.length < 2 || username.length > 30) errors.push('Please provide a username with between 2-30 characters.');
    if(password.length < 4) errors.push('Password must be 4 characters or more.');
    if(password !== repeatPassword) errors.push('Confirm Password field must match password field');
    setErrors(errors);
  }, [username, email, password, repeatPassword])

  const onSignUp = async (e) => {
    e.preventDefault();
    setHasSubmitted(true);
    if (!errors.length) {
      const data = await dispatch(signUp(username, email, password));
      if (data) {
        setErrors(data)
      }
    }
  };

  const updateUsername = (e) => {
    setUsername(e.target.value);
  };

  const updateEmail = (e) => {
    setEmail(e.target.value);
  };

  const updatePassword = (e) => {
    setPassword(e.target.value);
  };

  const updateRepeatPassword = (e) => {
    setRepeatPassword(e.target.value);
  };

  if (user) {
    return <Redirect to='/' />;
  }

  return (
    <form className='signup-form' onSubmit={onSignUp}>
      { hasSubmitted && <div>
        {errors.map((error, ind) => (
          <div key={ind}>{error}</div>
        ))}
      </div>}
      <div className='form-element'>
        <label>User Name</label>
        <input
          type='text'
          name='username'
          onChange={updateUsername}
          value={username}
        ></input>
      </div>
      <div className='form-element'>
        <label>Email</label>
        <input
          type='text'
          name='email'
          onChange={updateEmail}
          value={email}
        ></input>
      </div>
      <div className='form-element'>
        <label>Password</label>
        <input
          type='password'
          name='password'
          onChange={updatePassword}
          value={password}
        ></input>
      </div>
      <div className='form-element'>
        <label>Repeat Password</label>
        <input
          type='password'
          name='repeat_password'
          onChange={updateRepeatPassword}
          value={repeatPassword}
          required={true}
        ></input>
      </div>
      <button type='submit'>Sign Up</button>
    </form>
  );
};

export default SignUpForm;
