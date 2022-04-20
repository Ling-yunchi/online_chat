import fastapi
from socketio import AsyncServer, ASGIApp
from api.socket import add_event

# 创建socketio对象
sio = AsyncServer(
    cors_allowed_origins='*',  # 允许跨域
    async_mode='asgi'  # 异步模式
)


def mount_socketio(app: fastapi.FastAPI):
    add_event(sio)
    # 将socketio对象注册到app中
    app = ASGIApp(
        sio,
        app,
        socketio_path='/socket.io'
    )
    return app
