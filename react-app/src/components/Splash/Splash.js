import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {FaGithub, FaLinkedin} from 'react-icons/fa';
import './Splash.css'
import { createGameRequest } from '../../store/gameRequests';
import { login } from '../../store/session';
import { useHistory } from 'react-router-dom';




function Splash() {
  const dispatch = useDispatch()
  const history = useHistory()


  const sessionUser = useSelector(state => state.session.user);


  async function demoGame(e) {
    if(!sessionUser) {
      await dispatch(login('demo1@aa.io', 'password'));
    }
    let game = await dispatch(createGameRequest(-1));
    history.replace(`/games/${game.id}`);

  }


  return (
    <div className='home-page-container'>
      <h1>Welcome to JustChess!</h1>
      <p>The place you go when you just want to play chess.</p>
      <div className="home-outer-game-board">
        <div className="home-game-board">
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
          <div className="tile black-tile "></div>
          <div className="tile white-tile "></div>
        </div>
          <div className="piece" style={{position: 'relative', bottom:' 500px', left: '0px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/black,rook.png" alt='black rook'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 500px', left: '62.5px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/black,knight.png" alt='black knight'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 500px', left: '125px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/black,bishop.png" alt='black bishop'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 500px', left: '187.5px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/black,queen.png" alt='black queen'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 500px', left: '250px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/black,king.png" alt='black king'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 500px', left: '312.5px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/black,bishop.png" alt='black bishop'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 500px', left: '375px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/black,knight.png" alt='black knight'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 500px', left: '437.5px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/black,rook.png" alt='black rook'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 437.5px', left: '0px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/black,pawn.png" alt='black pawn'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 437.5px', left: '62.5px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/black,pawn.png" alt='black pawn'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 437.5px', left: '125px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/black,pawn.png" alt='black pawn'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 437.5px', left: '187.5px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/black,pawn.png" alt='black pawn'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 437.5px', left: '250px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/black,pawn.png" alt='black pawn'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 437.5px', left: '312.5px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/black,pawn.png" alt='black pawn'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 437.5px', left: '375px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/black,pawn.png" alt='black pawn'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 437.5px', left: '437.5px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/black,pawn.png" alt='black pawn'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 125px', left: '0px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/white,pawn.png" alt='white'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 125px', left: '62.5px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/white,pawn.png" alt='white'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 125px', left: '125px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/white,pawn.png" alt='white'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 125px', left: '187.5px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/white,pawn.png" alt='white'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 125px', left: '250px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/white,pawn.png" alt='white'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 125px', left: '312.5px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/white,pawn.png" alt='white'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 125px', left: '375px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/white,pawn.png" alt='white'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 125px', left: '437.5px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/white,pawn.png" alt='white'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 62.5px', left: '0px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/white,rook.png" alt='white rook'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 62.5px', left: '62.5px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/white,knight.png" alt='white knight'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 62.5px', left: '125px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/white,bishop.png" alt='white bishop'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 62.5px', left: '187.5px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/white,queen.png" alt='white queen'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 62.5px', left: '250px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/white,king.png" alt='white king'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 62.5px', left: '312.5px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/white,bishop.png" alt='white bishop'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 62.5px', left: '375px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/white,knight.png" alt='white knight'></img></div>
          <div className="piece" style={{position: 'relative', bottom:' 62.5px', left: '437.5px', visibility: 'visible'}}><img className="piece-img player-white" src="/images/white,rook.png" alt='white rook'></img></div>
        </div>
        <button className='new-game-button demo-game-button' onClick={demoGame}>Start Demo Game</button>
      {/* <p>when you just want to play chess.</p> */}
      <div className='about-area'>
        About
        <div className='about-links'>
          <a target='_blank' href='https://github.com/peter-monahan/Just-Chess'>
          <FaGithub size={25} />
          </a>
          <a target='_blank' href='https://www.linkedin.com/in/peter-monahan-8011bb235/'>
          <FaLinkedin size={25} />
          </a>
        </div>
      </div>
    </div>

  );
}
export default Splash;
