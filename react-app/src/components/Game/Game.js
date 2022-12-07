import { useState, useEffect } from 'react';
import { useHistory, useParams, Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {forfeiteGame, getAGame} from '../../store/games';
import GameBoard from './GameBoard';

import './Game.css'
function Game() {
  const dispatch = useDispatch();
  const { gameId } = useParams();
  const games = useSelector(state => state.games);
  const [game, setGame] = useState(undefined);
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState(false);
  const [playerColor, enemyColor] = game?.opponent.id === game?.white_id ? ['black', 'white'] : ['white', 'black'];
  const [dismiss, setDimiss] = useState(false);
  const sessionUser = useSelector(state => state.session.user);

  useEffect(() => {
      dispatch(getAGame(gameId));

  }, [gameId]);

  useEffect(() => {
    if(!game || game.id !== Number(gameId)) {
      setGame(games[gameId]);
    }
  }, [games, gameId]);

  useEffect(() => {
    if(games[gameId]) {
      const game = games[gameId];
      if(game) {
        if(game.data.checkmate) {
          setGameOver('checkmate');
          setWinner(game.data.winner);
        } else if(game.data.stalemate) {
          setGameOver('stalemate');
        } else if(game.data.forfeit) {
          setGameOver('resignation');
          setWinner(game.data.winner);
        } else if(gameOver.length) {
          setGameOver(false);
          setWinner(false);
        }
      }
    }
  }, [games, gameId]);

  const gameOverSplash = () => {
    const game = games[gameId];

    let string = '';
    if(gameOver === 'checkmate' || gameOver === 'resignation') {
      string = `${winner} wins by ${gameOver}`;
    } else if(gameOver === 'stalemate') {
      string = `draw by stalemate`;
    }
    return(
      <div className='game-over-container'>
        <div className='game-over-background'>
          <div className='game-over'>
            <div>{string}</div>
            <button>
            <Link to='/' >Return Home</Link>
            </button>
          </div>
        </div>
      </div>
    )
}
  if(game !== undefined && !(dismiss) ) {
    return (
      <div className='game-container'>
        <div className='game-player-div'>
          <img src={game.opponent.profile_image_url || `/images/${enemyColor},pawn.png`} className="user-icon-img"></img>
          <div>{game.opponent.username}<div className={`active-${games[gameId]?.opponent.active}`}></div></div>
        </div>
        {(gameOver && game !== undefined) && gameOverSplash()}
        <div className='board-container'>
        {(game !== undefined) && <GameBoard game={game} playerColor={playerColor} />}
        <button disabled={games[gameId] === undefined} onClick={() => dispatch(forfeiteGame(gameId))}>Resign</button>
        </div>
        <div className='game-player-div'>
          <img src={sessionUser.profile_image_url || `/images/${playerColor},pawn.png`} className="user-icon-img"></img>
          <div>{sessionUser.username}</div>
        </div>
      </div>
    );
  } else {
    return null;
  }
}
export default Game;
