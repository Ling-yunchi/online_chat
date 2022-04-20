from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.ChatModel import get_chat_rooms, ChatRoomBean, ChatRoom, get_messages
from utils.auth import oauth2_scheme, get_current_user
from utils.database import get_db

router = APIRouter(
    prefix='/chat',
    tags=['chat'],
)


@router.get('/rooms', tags=['room'], dependencies=[Depends(oauth2_scheme)])
async def get_rooms(name: str, page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    return get_chat_rooms(db, name, page - 1, page_size)


@router.get("/room/{room_id}", tags=['room'], dependencies=[Depends(oauth2_scheme)])
async def get_room(room_id: int, db: Session = Depends(get_db)):
    room: ChatRoom = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if room is None:
        return {"msg": "room not found"}
    return room


@router.post("/room", tags=['room'], dependencies=[Depends(oauth2_scheme)])
async def create_room(room_bean: ChatRoomBean, db: Session = Depends(get_db)):
    new_room = ChatRoom(**room_bean.dict())
    new_room.created_time = datetime.now()
    new_room.online_num = 0
    db.add(new_room)
    db.commit()
    return {"msg": "success"}


@router.put("/room/{room_id}", tags=['room'], dependencies=[Depends(oauth2_scheme)])
async def update_room(room_id: int, room_bean: ChatRoomBean, db: Session = Depends(get_db)):
    room: ChatRoom = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if room is None:
        return {"msg": "room not found"}
    room.name = room_bean.name
    room.description = room_bean.description
    db.commit()
    return {"msg": "success"}


@router.delete("/room/{room_id}", tags=['room'])
async def delete_room(room_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(db, token)
    if user is None:
        return {"msg": "user not found"}
    room: ChatRoom = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    if room is None:
        return {"msg": "room not found"}
    if user.id != room.create_user_id:
        return {"msg": "no permission"}
    db.delete(room)
    db.commit()
    return {"msg": "success"}


@router.get("/room/{room_id}/messages", tags=['room'], dependencies=[Depends(oauth2_scheme)])
async def get_room_messages(room_id: int, page: int = 1, page_size: int = 1000, db: Session = Depends(get_db)):
    return get_messages(db, room_id, page - 1, page_size)
