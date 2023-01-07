import { useState, useEffect } from "react";
import { useDispatch, useSelector } from 'react-redux';
import { Link, useHistory } from "react-router-dom";
import {getAllGameRequests, deleteAGameRequest, createGameRequest} from '../../../store/gameRequests'
import {getAllGames, acceptGameRequest} from '../../../store/games';
import {getAllFriends} from '../../../store/friends';
import './GamesBar.css';
import { getAUser } from "../../../store/users";

function GamesBar({setDisplay}) {
  const dispatch = useDispatch();
  const history = useHistory();
  const [requestsType, setRequestsType] = useState('received');
  const gameRequests = useSelector(state => state.gameRequests);
  const games = useSelector(state => state.games);
  const friends = useSelector(state => state.friends);
  const [showFriends, setShowFriends] = useState(false);
  const [showOptions, setShowOptions] = useState(false);
  const [showBots, setShowBots] = useState(false);
  const [bot, setBot] = useState(1);
  const sessionUser = useSelector(state => state.session.user);

  function handleClick(e) {
    const targ = e.target;
    if(!(targ.id.startsWith('game-bar'))){
      setDisplay(false);
    }
  }

  const acceptButton = async (requestId) => {
    const id = await dispatch(acceptGameRequest(requestId))
    history.replace(`/games/${id}`);
  }


  useEffect(() => {
    document.addEventListener('click', handleClick);
    dispatch(getAllGames())
    dispatch(getAllGameRequests())

    return () => {
      document.removeEventListener('click', handleClick)
    }
  }, [])


  const ReceivedRequests = () => (
    <>
      {Object.keys(gameRequests.received).map(key => {
        const request = gameRequests.received[key];
        return (
          <div key={key} id='game-bar' className="game-request">
            {request.sender.username}
            <div id='game-bar'>
            <button onClick={() => acceptButton(request.id).then(() => dispatch(getAUser(request.user_id)))}>Accept</button>
            <button onClick={() => dispatch(deleteAGameRequest(request.id)).then(() => dispatch(getAUser(request.user_id)))} id="game-bar">Decline</button>
            </div>
          </div>
        )
      })}
    </>
  )

  const SentRequests = () => (
    <>
      {Object.keys(gameRequests.sent).map(key => {
        const request = gameRequests.sent[key];
        return (
          <div key={key} id='game-bar' className="game-request">
            {request.receiver.username}
            <button onClick={() => dispatch(deleteAGameRequest(request.id)).then(() => dispatch(getAUser(request.opponent_id)))} id='game-bar'>Delete</button>
          </div>
        )
      })}
    </>
  )

  const Games = () => (
    <>
      {Object.keys(games).map(key => {
        const game = games[key];
        const [playerColor, enemyColor] =( game?.opponent.id === game?.white_id) || game?.white_id === null ? ['black', 'white'] : ['white', 'black'];
        const yourTurn = game.data.turn[0] === playerColor;
        return (
          <Link className="game-button" to={`/games/${game.id}`} key={key}>
            {game.opponent.username}<div className={`active-${game.opponent.active}`}></div>
            <div className="turn-text">{ yourTurn ? 'Your turn' : `${game.opponent.username}'s turn`}</div>
          </Link>
        )
      })}
    </>
  )

  const Friends = () => (
    <div id="game-bar" className="game-friends-list">
      {Object.keys(friends).map(key => {
        const friend = friends[key];
        return (
          <button disabled={Object.keys(gameRequests.sent).some(key => gameRequests.sent[key].opponent_id === friend.id) || Object.keys(gameRequests.received).some(key => gameRequests.received[key].user_id === friend.id)} id="game-bar" onClick={(e) => {dispatch(createGameRequest(friend.id)); setShowFriends(false); setRequestsType('sent'); e.stopPropagation();}} key={key}>
            {friend.username}<div id="game-bar" className={`active-${friend.active}`}></div>
          </button>
        )
      })}
      </div>
  )
  const Bots = () => (
    <div id="game-bar--bots-area" className="game-bots-slider">
      Difficulty: {bot}
      <input id="game-bar--bots-area" type="range" min={1} max={5} value={bot} onChange={e => setBot(e.target.value)} />
      <button id="game-bar--bots-area" disabled={bot > 1} onClick={ e => {dispatch(createGameRequest(-bot)); setDisplay(false); e.stopPropagation();}}>Play Bot</button>
      {bot > 1 && 'Coming Soon!'}
    </div>
  )
  const optionsClick = (e) => {
    setShowOptions(false);
  }
  const friendsClick = e => {
    setShowFriends(false);
  }
  const botsClick = e => {
    if(!e.target.id.endsWith('bots-area')) {
      setShowBots(false);
    }
  }
  useEffect(() => {
    if(showOptions) {
      document.addEventListener('click', optionsClick);

      return () => {
        document.removeEventListener('click', optionsClick)
      }
    }
    if(showFriends) {
      document.addEventListener('click', friendsClick);

      return () => {
        document.removeEventListener('click', friendsClick)
      }
    }
    if(showBots) {
      document.addEventListener('click', botsClick);

      return () => {
        document.removeEventListener('click', botsClick)
      }
    }

  }, [showOptions, showFriends, showBots])

  const newGameClick = () => {
    setShowOptions(true);
  }



  const newGameButton = (
    <button id='game-bar' className="new-game-button" onClick={newGameClick}>
      New Game
      {showOptions && <div id="game-bar" className="game-options-container"><div id="game-bar" className="game-options"><button id="game-bar" onClick={() => {setShowFriends(true); dispatch(getAllFriends())}}>With a Friend</button>{/*<button id="game-bar" onClick={() => dispatch(createGameRequest(0))}>Random Player</button>*/}<button id="game-bar" onClick={() => setShowBots(true)}>With a Bot</button></div></div>}
      {showFriends && <div id="game-bar" className="game-options-container"><div id="game-bar" className="game-options"><Friends /></div></div>}
      {showBots && <div id="game-bar" className="game-options-container"><div id="game-bar" className="game-options"><Bots /></div></div>}
    </button>
  )

  return (
    <div className="game-bar" id="game-bar">
      {true && newGameButton}
      <div id='game-bar' className="game-requests">
        Game Invites
        <div className="game-sent-received" id="game-bar">
          <div onClick={(e) => setRequestsType('received')} className={`game-received game-tab ${requestsType === 'received' ? 'active' : ''}`} id="game-bar">Received</div>
          <div onClick={(e) => setRequestsType('sent')} className={`game-sent game-tab ${requestsType === 'sent' ? 'active' : ''}`} id="game-bar">Sent</div>
        </div>
        <div className="game-requests-info" id="game-bar">
          {requestsType === 'received' ? <ReceivedRequests /> : <SentRequests />}
        </div>
      </div>
      <div id='game-bar' className="games">
        Games
        <div className="games-info" id="game-bar">
          <Games />
        </div>
      </div>
    </div>
  );
}

export default GamesBar
