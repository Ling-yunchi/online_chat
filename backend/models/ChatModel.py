from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session

from models.UserModel import User
from utils.database import Base

'''
    ChatSchema
'''


class ChatRoomBean(BaseModel):
    name: str
    create_user_id: int
    description: str


class ChatMessageResult(BaseModel):
    id: int
    user_id: int
    user_name: str
    avatar: str
    message: str
    time: str


'''
    ChatModel
'''


class ChatRoom(Base):
    __tablename__ = 'chat_room'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    create_user_id = Column(Integer, nullable=False)
    description = Column(String(500), nullable=True)
    created_time = Column(DateTime, nullable=False)
    online_num = Column(Integer, nullable=False, default=0)


class ChatMessage(Base):
    __tablename__ = 'chat_message'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    chat_room_id = Column(Integer, nullable=False)
    message = Column(String(255), nullable=False)
    time = Column(DateTime, nullable=False)


'''
    ChatDao
'''


def get_chat_room(db: Session, chat_room_id: int):
    return db.query(ChatRoom).filter(ChatRoom.id == chat_room_id).first()


def get_chat_rooms(db: Session, name: str, page: int, page_size: int):
    return db.query(ChatRoom) \
        .filter(ChatRoom.name.like(f'%{name}%')) \
        .order_by(ChatRoom.created_time.desc()) \
        .offset(page * page_size) \
        .limit(page_size) \
        .all()


def get_messages(db: Session, chat_room_id: int, page: int, page_size: int):
    return db.query(ChatMessage.id, User.id.label("user_id"), User.username,
                    User.avatar, ChatMessage.message, ChatMessage.time) \
        .join(User, ChatMessage.user_id == User.id) \
        .filter(ChatMessage.chat_room_id == chat_room_id) \
        .order_by(ChatMessage.time.desc()) \
        .offset(page * page_size) \
        .limit(page_size) \
        .all()
