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
  const [showFriends, setShowFriends] = useState(false);
  const [showOptions, setShowOptions] = useState(false);
  const sessionUser = useSelector(state => state.session.user);

  function handleClick(e) {
    const targ = e.target;
    if(!(targ.id === 'game-bar')){
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
        const [playerColor, enemyColor] = game?.opponent.id === game?.white_id ? ['black', 'white'] : ['white', 'black'];
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

  const optionsClick = (e) => {
    setShowOptions(false);
  }
  const friendsClick = e => {
    setShowFriends(false);
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

  }, [showOptions, showFriends])

  const newGameClick = () => {
    setShowOptions(true);
  }



  const newGameButton = (
    <button id='game-bar' className="new-game-button" onClick={newGameClick}>
      New Game
      {showOptions && <div id="game-bar" className="game-options-container"><div id="game-bar" className="game-options"><button id="game-bar" onClick={() => {setShowFriends(true); dispatch(getAllFriends())}}>With a Friend</button><button id="game-bar" onClick={() => dispatch(createGameRequest(-0))}>Random Player</button><button id="game-bar" onClick={() => {dispatch(createGameRequest(-0)); setDisplay(false)}}>With a Bot</button></div></div>}
      {showFriends && <div id="game-bar" className="game-options-container"><div id="game-bar" className="game-options">friends</div></div>}
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
