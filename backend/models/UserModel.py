from pydantic import BaseModel
from pydantic.class_validators import Optional
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session

from utils.database import Base

'''
    User Schema
'''


class UserBean(BaseModel):
    username: str
    password: str
    avatar: Optional[str] = None


class LoginBean(BaseModel):
    name: str
    password: str


class UserInfo(BaseModel):
    id: int
    avatar: Optional[str] = None
    username: str


'''
    User Model
'''


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    online = Column(Boolean, default=False)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, password={self.password})"


'''
    User Dao
'''


def get_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def save(db: Session, user: User):
    if u := db.query(User).filter(User.id == user.id).first():
        raise Exception("User already exists")
    db.add(user)
    db.commit()


def update(db: Session, user: User):
    if user := db.query(User).filter(User.id == user.id).first():
        user.username = user.username
        user.password = user.password
        user.email = user.email
        user.role = user.role
        db.commit()
    else:
        raise Exception("User not found")


def delete(db: Session, user_id: int):
    if user := db.query(User).filter(User.id == user_id).first():
        db.delete(user)
        db.commit()
    else:
        raise Exception("User not found")


def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
