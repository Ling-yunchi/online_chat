from datetime import datetime

import socketio
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.ChatModel import ChatRoom, ChatMessage
from models.UserModel import User
from utils.auth import get_current_user
from utils.database import SessionLocal


def add_event(sio: socketio.Server):
    @sio.on('connect')
    async def connect(sid, environ, auth, db: Session = SessionLocal()):
        print('connect ', sid)
        if token := auth['token'].replace('Bearer ', ''):
            if user := get_current_user(db, token):
                # add user to session
                await sio.save_session(sid, {'user_id': user.id, 'username': user.username})
                # check auth and update online status
                db.query(User).filter(User.id == user.id).update({User.online: True})
                db.commit()
                print(f'user {user.id} connected')
            else:
                await sio.disconnect(sid)
        else:
            await sio.disconnect(sid)
        db.close()

    @sio.on('disconnect')
    async def disconnect(sid, db: Session = SessionLocal()):
        print('disconnect ', sid)
        # get user from dict
        session = await sio.get_session(sid)
        user_id = session['user_id']
        # update online status
        db.query(User).filter(User.id == user_id).update({User.online: False})
        db.commit()
        print(f'user {user_id} disconnected')
        db.close()

    chat_api(sio)


def chat_api(sio: socketio.Server):
    @sio.on('enter_room')
    async def enter_room(sid, room_id, db: Session = SessionLocal()):
        room: ChatRoom = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
        if not room:
            await sio.emit('enter_room', {'success': False, 'msg': 'Room not found'}, room=sid)
            return
        session = await sio.get_session(sid)
        print(session['username'], ' enter room ', room_id)
        sio.enter_room(sid, room_id)
        await sio.emit('enter_room', {'success': True, 'msg': 'success'}, room=sid)
        await sio.emit('room_info', f"{session['username']} enter the room {room.name}", room=str(room_id))

        room.online_num += 1
        db.commit()
        db.close()

    @sio.on('leave_room')
    async def leave_room(sid, room_id, db: Session = SessionLocal()):
        room: ChatRoom = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
        if not room:
            await sio.emit('leave_room', {'success': False, 'msg': 'Room not found'}, room=sid)
            return
        print('leave room ', room.name)
        sio.leave_room(sid, room)
        session = await sio.get_session(sid)
        await sio.emit('room_info', f"{session['username']} leave the room {room.name}", room=str(room_id))
        room.online_num -= 1
        db.commit()
        db.close()

    @sio.on('send_message')
    async def send_message(sid, data, db: Session = SessionLocal()):
        print('send message ', data)
        session = await sio.get_session(sid)
        user_id = session['user_id']
        if user_id != data['user_id']:
            await sio.emit('errorMessage', {'success': False, 'msg': 'Invalid user_id or room_id'}, room=sid)
            return
        user = db.query(User).filter(User.id == user_id).first()
        room_id = data['room_id']
        message = data['message']
        time = datetime.now()
        chat_message = ChatMessage(user_id=user_id,
                                   chat_room_id=room_id,
                                   message=message,
                                   time=time)
        db.add(chat_message)
        db.commit()
        db.flush()
        await sio.emit('room_message', {
            'id': chat_message.id,
            'user_id': user.id,
            'username': user.username,
            'avatar': user.avatar,
            'message': message,
            'time': time.isoformat()
        }, room=str(room_id))
        db.close()
