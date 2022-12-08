import { useState, useEffect } from 'react';
import { useHistory, useParams, Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {forfeiteGame, getAGame, makeAMove} from '../../store/games';
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
  const [upgrade, setUpgrade] = useState(null);

  const sessionUser = useSelector(state => state.session.user);

  useEffect(() => {
      dispatch(getAGame(gameId));
  }, [gameId]);

  useEffect(() => {
    // if(!game || game.id !== Number(gameId)) {
    //   setGame(games[gameId]);
    // }
    let timeout;
    const func = async () => {
      timeout = setTimeout(() => {
        setGame(games[gameId]);
      }, 600);
    }
    func()

  }, [games, gameId]);

  useEffect(() => {
    setUpgrade(null)
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


    let string = '';
    if(gameOver === 'checkmate' || gameOver === 'resignation') {
      string = `${winner} wins by ${gameOver}`;
    } else if(gameOver === 'stalemate') {
      string = `draw by stalemate`;
    }
    return(
      <div className='splash-container'>
        <div className='splash-background'>
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

const upgradePieceSplash = () => {
  return(
    <div className='splash-container'>
      <div className='splash-background'>
        <div className='upgrade-piece'>
          <div className='upgrade-pieces'>
          <img className='black-pawn-img' onClick={() => dispatch(makeAMove(upgrade.gameId, {...upgrade.move, piece: 'knight'}))} id='chess-board' src={`/images/${playerColor},knight.png`} alt='knight' ></img>
          <img className='black-pawn-img' onClick={() => dispatch(makeAMove(upgrade.gameId, {...upgrade.move, piece: 'rook'}))} id='chess-board' src={`/images/${playerColor},rook.png`} alt='rook' ></img>
          <img className='black-pawn-img' onClick={() => dispatch(makeAMove(upgrade.gameId, {...upgrade.move, piece: 'bishop'}))} id='chess-board' src={`/images/${playerColor},bishop.png`} alt='bishop' ></img>
          <img className='black-pawn-img' onClick={() => dispatch(makeAMove(upgrade.gameId, {...upgrade.move, piece: 'queen'}))} id='chess-board' src={`/images/${playerColor},queen.png`} alt='queen' ></img>
          </div>
          <button onClick={() => setUpgrade(null)}>Cancel</button>
        </div>
      </div>
    </div>
  )
}

  if(game !== undefined) {
    return (
      <div className='game-container'>
        <div className='game-player-div'>
          <img src={game.opponent.profile_image_url || `/images/${enemyColor},pawn.png`} className="user-icon-img"></img>
          <div>{game.opponent.username}<div className={`active-${games[gameId]?.opponent.active}`}></div></div>
        </div>
        {(gameOver && game !== undefined) && gameOverSplash()}
        {(upgrade && game !== undefined) && upgradePieceSplash()}
        <div className='board-container'>
        {(game !== undefined) && <GameBoard setUpgrade={setUpgrade} game={game} playerColor={playerColor} />}
        <button disabled={gameOver !== false} onClick={() => dispatch(forfeiteGame(gameId))}>Resign</button>
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
