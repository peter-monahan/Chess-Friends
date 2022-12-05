import { useState, useEffect } from 'react';
import { useHistory, useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { makeAMove } from '../../store/games';
import Piece from './Piece';



function GameTile({game, row, col, selected, setSelected}) {
  const liveGame = useSelector(state => state.games[game.id])
  const dispatch = useDispatch()
  const color = ((row+col) % 2) === 0 ? 'white' : 'black';

  const [valid, setValid] = useState('');

  useEffect(() => {
    const mostRecent = liveGame.data.history[liveGame.data.history.length-1]


    if( selected && liveGame.data.pieces[selected.color][selected.pieceStr].valid_moves.some(coord => coord.join(',') === `${row},${col}`)) {
      setValid('tile-valid valid')
    } else if (selected && liveGame.data.pieces[selected.color][selected.pieceStr].curr_coords.join(',') === `${row},${col}`) {
      setValid('tile-selected')
    } else if( mostRecent && mostRecent.some(coord => coord.join(',') === `${row},${col}`)) {
      setValid('tile-moved')
    } else if(valid.length) {
      setValid('');
    }

  }, [selected, liveGame]);



  const handleClick = (e) => {
    if(selected && valid.length) {
      dispatch(makeAMove(game.id, [selected.coords, [row, col]]))
    }
    setSelected(null);
  }
  return (
    <div className={`tile ${color}-tile ${valid}`} id={`chess-board`} onClick={handleClick}>

    </div>
  );
}
export default GameTile;
