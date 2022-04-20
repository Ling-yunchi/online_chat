from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from models import UserModel
from models.UserModel import User, UserBean, UserInfo
from utils.auth import get_current_user, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    get_password_hash, oauth2_scheme
from utils.database import get_db

router = APIRouter(
    prefix='/user',
    tags=['user'],
)


@router.get('/users')
async def get_users(db: Session = Depends(get_db)):
    user_list: list[User] = db.query(User).all()
    user_bean_list = [UserInfo(**user.__dict__) for user in user_list]
    return user_bean_list


@router.get("/username")
async def check_username_exist(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        return {"username": username, "exists": False}
    return {"username": username, "exists": True}


@router.post("/register")
async def register_user(user_bean: UserBean, db: Session = Depends(get_db)):
    user = User(**user_bean.dict())
    user.password = get_password_hash(user.password)
    try:
        UserModel.save(db, user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return {"message": "User created successfully"}


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": user.id, "username": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def me(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    print(token)
    current_user = get_current_user(db, token)
    return UserInfo(id=current_user.id, username=current_user.username,avatar=current_user.avatar)
