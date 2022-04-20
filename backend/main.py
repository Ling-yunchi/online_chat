from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from api import api
from utils import database
from utils.socket import mount_socketio

database.Base.metadata.create_all(database.engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return HTMLResponse(
        f"<h1><center>Welcome to Online Chat</center></h1>"
        f"<center>please go to <a href='/docs'>docs</a> for more information</center>"
    )


app.include_router(api)

app = mount_socketio(app)
