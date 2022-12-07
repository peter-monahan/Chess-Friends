import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import './Splash.css'
function Splash() {
  const dispatch = useDispatch()


  const sessionUser = useSelector(state => state.session.user);




  return (
    <div className='home-page-container'>
      <h1>Welcome to JustChess!</h1>
      <p>The place you go...</p>
      <div class="home-outer-game-board">
        <div class="home-game-board">
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
          <div class="tile black-tile "></div>
          <div class="tile white-tile "></div>
        </div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 500px', left: '0px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/black,rook.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 500px', left: '62.5px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/black,knight.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 500px', left: '125px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/black,bishop.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 500px', left: '187.5px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/black,queen.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 500px', left: '250px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/black,king.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 500px', left: '312.5px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/black,bishop.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 500px', left: '375px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/black,knight.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 500px', left: '437.5px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/black,rook.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 437.5px', left: '0px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/black,pawn.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 437.5px', left: '62.5px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/black,pawn.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 437.5px', left: '125px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/black,pawn.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 437.5px', left: '187.5px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/black,pawn.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 437.5px', left: '250px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/black,pawn.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 437.5px', left: '312.5px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/black,pawn.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 437.5px', left: '375px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/black,pawn.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 437.5px', left: '437.5px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/black,pawn.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 125px', left: '0px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/white,pawn.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 125px', left: '62.5px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/white,pawn.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 125px', left: '125px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/white,pawn.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 125px', left: '187.5px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/white,pawn.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 125px', left: '250px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/white,pawn.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 125px', left: '312.5px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/white,pawn.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 125px', left: '375px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/white,pawn.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 125px', left: '437.5px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/white,pawn.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 62.5px', left: '0px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/white,rook.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 62.5px', left: '62.5px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/white,knight.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 62.5px', left: '125px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/white,bishop.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 62.5px', left: '187.5px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/white,queen.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 62.5px', left: '250px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/white,king.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 62.5px', left: '312.5px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/white,bishop.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 62.5px', left: '375px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/white,knight.png"></img></div>
          <div class="black-pawn" style={{position: 'relative', bottom:' 62.5px', left: '437.5px', visibility: 'visible'}}><img class="black-pawn-img player-white" src="/images/white,rook.png"></img></div>
        </div>
      <p>when you just want to play chess.</p>

    </div>

  );
}
export default Splash;
