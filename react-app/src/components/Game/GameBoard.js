import { useState, useEffect } from 'react';
import { useHistory, useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { makeAMove } from '../../store/games';
import Piece from './Piece';
import GameTile from './GameTile';


function GameBoard({game, playerColor, setUpgrade, gameOver}) {
  // const dispatch = useDispatch()
  const [selected, setSelected] = useState(null)
  const tiles = [];
  const pieces = [];
  for(let row = 0; row < 8; row++) {
    for(let col = 0; col < 8; col++) {
      const pieceStr = game.data.board[row][col]
      if(pieceStr) {
        pieces.push(
          <Piece key={`${row},${col}`} gameOver={gameOver} setUpgrade={setUpgrade} start={[row, col]} pieceStr={pieceStr} game={game} selected={selected} setSelected={setSelected} playerColor={playerColor} />
        )
      }
      tiles.push(
        <GameTile setUpgrade={setUpgrade} key={`${row},${col}`} selected={selected} setSelected={setSelected} game={game} row={row} col={col} />
      )
    }
  }
  function handleClick(e) {
    const targ = e.target;
    if(!(targ.id.startsWith('chess-board'))){
      setSelected(null)
    }

  }
  useEffect(() => {
    document.addEventListener('click', handleClick);

    return () => {
      document.removeEventListener('click', handleClick)
    }
  }, [])

  return (
    <div className={`outer-game-board player-${playerColor}`}>
      <div className='game-board'>
      {tiles}
      </div>
      {pieces}
    </div>
  );
}
export default GameBoard;





//     console.log(selected)



  // {/* {boardLen.map((el, rowIndex) => {
  //   return (
    //     <div className='game-board-row ' key={rowIndex}>
    //       {boardLen.map((el, colIndex) => {
      //         const color = ((rowIndex+colIndex) % 2) === 0 ? 'white' : 'black';
  //         const pieceStr = game.data.board[rowIndex][colIndex]
  //         const classStr = pieceStr || ''
  //         return (
  //           <div className={`tile ${color}-tile`} data-type={'tile'} data-coords={`${rowIndex},${colIndex}`} id={`chess-board`} key={colIndex}>
  //                 { pieceStr !== null && <Piece start={[rowIndex, colIndex]} pieceStr={pieceStr} game={game} />}
  //           </div>
  //         )
  //       })}
  //     </div>
  //   )
// })} */}
