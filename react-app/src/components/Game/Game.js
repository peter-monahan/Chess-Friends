import { useState, useEffect } from 'react';
import { useHistory, useParams } from 'react-router-dom';
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
  const [playerColor, enemyColor] = game?.opponent.id === game?.white_id ? ['black', 'white'] : ['white', 'black'];
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
      if(game.data.checkmate) {
        setGameOver('checkmate')
      } else if(game.data.stalemate) {
        setGameOver('stalemate')
      } else if(game.data.forfeit) {
        setGameOver('forfeit')
      }
    }
  }, [games]);

  const gameOverSplash = () => {
    const game = games[gameId];
    let string = ''
    let winner;
    if(gameOver === 'checkmate' || gameOver === 'forfeit') {
      winner = game.data.winner;
      string = `${winner} wins by ${gameOver}`
    } else if(gameOver === 'stalemate') {
      string = `draw by stalemate`
    }
    return(
      <div className='game-over'>
        {string}
      </div>
    )
}
  if(game !== undefined) {
    return (
      <div>
        {gameOver && gameOverSplash()}
        <div className='game-player-div'>
          <img src={game.opponent.profile_image_url || `/images/${enemyColor},pawn.png`} className="user-icon-img"></img>
          <div>{game.opponent.username}<div className={`active-${games[gameId]?.opponent.active}`}></div></div>
        </div>
        <div className='board-container'>
        <GameBoard game={game} playerColor={playerColor} />
        <button onClick={() => dispatch(forfeiteGame(gameId))}>Forfeit</button>
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
