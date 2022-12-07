import { useState, useEffect } from 'react';
import { useHistory, useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { makeAMove } from '../../store/games';

function getTransform(startCoords, piece) {
  // return `0px,0px`;
  if(!piece) return `0px,0px`;
  const [startRow, startCol] = startCoords;
  const [row, col] = piece.curr_coords;
  const [newRow, newCol] = [startRow-row, col-startCol];
  const [pxcol, pxrow] = [(0 + (newCol*62.5)), (0 - (newRow*62.5))]
  return `${pxcol}px,${pxrow}px`
}
function getPosition(start) {
  let bottom = 500
  let left = 0

  bottom -= (start[0] * 62.5)
  left += start[1] * 62.5


  bottom = `${bottom}px`
  left = `${left}px`
  return {bottom, left}
}

function Piece({start, pieceStr, game, selected, setSelected, playerColor}) {
  const dispatch = useDispatch()
  const liveGame = useSelector(state => state.games[game.id])
  const color = pieceStr.slice(0,5)
  const piece = liveGame?.data.pieces[color][pieceStr]
  const [valid, setValid] = useState('');

  let owned;
  if(game.opponent.id === game.black_id) {
    if(color === 'white') {
      owned = true;
    } else {
      owned = false
    }
  } else {
    if(color === 'black') {
      owned = true;
    } else {
      owned = false
    }
  }
  useEffect(() => {
    if(selected && piece) {
      if(liveGame.data.pieces[selected.color][selected.pieceStr].valid_moves.some(coord => coord.join('') === piece.curr_coords.join(''))) {
        setValid('piece-valid valid')
      } else if(valid.length) {
        setValid('');
      }
    } else if(valid.length) {
      setValid('');
    }
  }, [selected, liveGame]);

  const handleClick = (e) => {
    if(owned && color === liveGame.data.turn[0]) {
      setSelected({pieceStr, color, coords: piece.curr_coords})
    } else if(!owned && selected && valid.length) {
      dispatch(makeAMove(game.id, [selected.coords, piece.curr_coords]))
      setSelected(null)
    } else if(selected) {
      setSelected(null)
    }
    // e.stopPropagation()
  }
  const styleObj = {
    position: 'relative',
    transform: `translate(${getTransform(start, piece)})`,
    ...getPosition(start),
    visibility: piece ? 'visible' : 'hidden',
  }

  return (
    <div id='chess-board' style={styleObj} className='black-pawn'>
      <img className={`black-pawn-img player-${playerColor}`} onClick={handleClick} id={`chess-board`} src={`/images/${pieceStr.slice(0,pieceStr.length-3)}.png`} ></img>
    </div>
  );
}
export default Piece;

// data-type={'piece'} data-color={color} data-piecestr={pieceStr} data-coords={piece.curr_coords}
