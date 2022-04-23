from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from api import api
from utils import database
from utils.socket import mount_socketio

# 通过数据实体创建数据库表
database.Base.metadata.create_all(database.engine)

app = FastAPI()
# 添加跨域中间件
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

# 添加路由
app.include_router(api)
# 挂载socketio服务
app = mount_socketio(app)
