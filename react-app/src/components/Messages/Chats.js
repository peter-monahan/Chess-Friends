import { useEffect, useState } from 'react';
import { NavLink } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { getAllChats, createChat, deleteAChat } from '../../store/chats';
import { createMessage, deleteAMessage, getAllMessages, editMessage } from '../../store/messages';
import {getAllFriendRequests} from '../../store/friendRequests';
import {getAllFriends} from '../../store/friends';
import {getAllGameRequests} from '../../store/gameRequests';
function Chats() {
  const dispatch = useDispatch()
  const [thing, setThing] = useState('')
  const messages = useSelector(state => state.messages)
  const user = useSelector(state => state.session.user)
  useEffect(() => {
    if(user) {

      dispatch(getAllFriends())
      dispatch(getAllChats())
      dispatch(getAllFriendRequests())
      dispatch(getAllGameRequests())
      if (user.id === 1){
        dispatch(getAllMessages(3))
      } else if (user.id === 3) {
        dispatch(getAllMessages(1))
      }
    }
  }, [user])

  const doThing = () => {
    if (user.id === 1) {
      console.log('id=1')
      dispatch(deleteAChat(4))
    }
    if (user.id === 3) {
      console.log('id=3')
      dispatch(deleteAChat(5))
    }

  }
  const doOtherThing = () => {
    if (user.id === 1) {
      console.log('id=1')
      dispatch(createChat(3))
    }
  }
  const messageDel = () => {
      dispatch(deleteAMessage(thing))
  }
  const messageCreate = () => {
      dispatch(createMessage({content: 'first'}, thing))
  }
  const messageEdit = () => {
    dispatch(editMessage({content: 'edited'}, thing))
}
  return (
    <div>
      <button onClick={doThing}>del</button>
      <button onClick={doOtherThing}>create</button>
      <button onClick={messageDel}>message del</button>
      <button onClick={messageCreate}>message create</button>
      <button onClick={messageEdit}>message edit</button>

      <input value={thing} onChange={e => setThing(e.target.value)}></input>


      {Object.keys(messages).map(key => {
        return (
          <div>
            {key}
            {Object.keys(messages[key]).map(messKey => {
              let message = messages[key][messKey]
              return (
                <div style={{border: '1px solid black'}}>
                  <div>id:{message.id}</div>
                  <div>sender:{message.sender_id}</div>
                  <div>receiver:{message.receiver_id}</div>
                  <div>content:{message.content}</div>
                </div>
              )
            })}
          </div>
        )
      })}
    </div>
  );
}

export default Chats;
