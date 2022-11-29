import { useState, useEffect } from 'react';
import { useHistory, useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {getAGame} from '../../store/games';

import './Game.css'
function Game() {
  const history = useHistory()
  const dispatch = useDispatch()
  const { gameId } = useParams();
  const games = useSelector(state => state.games)
  const boardLen = new Array(8).fill(1)

  useEffect(() => {
    dispatch(getAGame(gameId));
  }, [gameId])


  return (
<div>
  <div className='game-board'>
    {boardLen.map((el, rowIndex) => {
      return (
        <div className='game-board-row ' key={rowIndex}>
          {boardLen.map((el, colIndex) => {
            const color = ((rowIndex+colIndex) % 2) === 0 ? 'white' : 'black';
            const pieceStr = games[gameId]?.json_data.board[rowIndex][colIndex]
            const classStr = pieceStr || ''
            return (
              <div style={{backgroundImage: `url(images/white,Pawn.png`, color: 'black'}} className={`tile ${color}-tile ${classStr.slice(0,classStr.length-3)}`} id={`${rowIndex},${colIndex}`} key={colIndex}>
                {pieceStr}
              </div>
            )
          })}
        </div>
      )
    })}
  </div>
</div>
  );
}
export default Game;
