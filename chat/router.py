import json
from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from auth.models import User

from chat.models import Message
from database import async_session_maker, get_async_session

from dependencies.auth_dependency import current_user


router = APIRouter(prefix="/chat", tags=['chat'])

templates = Jinja2Templates(directory="templates")  


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket

    def disconnect(self, websocket: WebSocket, username: str):
        del self.active_connections[username]

    async def send_personal_message(self, message: str, username: str):
        if username in self.active_connections:
            websocket = self.active_connections[username]
            await websocket.send_text(message)

    async def broadcast(self, message: str, add_to_database: bool, username: str):
        if add_to_database:
            await self.add_message_to_database(message, username)
        for connection in self.active_connections:
            websocket = self.active_connections[connection]
            await websocket.send_text(message)

    async def add_message_to_database(self, message: str, username: str):
        async with async_session_maker() as session:
            statement = insert(Message).values(message=message, username=username)
            await session.execute(statement)
            await session.commit()
                

manager = ConnectionManager()


@router.get('/last_messages')
async def get_last_messages(session: AsyncSession = Depends(get_async_session)):
    query = select(Message).order_by(Message.id.desc()).limit(10)

    result = await session.execute(query)
    messages = result.all()
    messages_list = [message[0].as_dict() for message in messages]

    return messages_list


@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            message_username = message_data.get('username', username)
            message = message_data.get('message', '')

            await manager.broadcast(f"User {message_username}: {message}", add_to_database=True, username=message_username)
    except WebSocketDisconnect:
        manager.disconnect(websocket, username)
        await manager.broadcast(f"User {username} left the chat", add_to_database=False)


@router.get('/')
def get_chat_page(request: Request):
    return templates.TemplateResponse('chat.html', {"request": request})