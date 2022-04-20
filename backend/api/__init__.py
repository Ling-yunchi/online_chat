from fastapi import APIRouter

from api import user, chat

api = APIRouter(
    prefix="/api"
)
api.include_router(user.router)
api.include_router(chat.router)