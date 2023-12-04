from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from chat.models import Message
from database import async_session_maker, get_async_session


router = APIRouter(prefix="/chat", tags=['chat'])

templates = Jinja2Templates(directory="templates")


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, add_to_database: bool):
        if add_to_database:
            await self.add_message_to_database(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def add_message_to_database(message: str):
        async with async_session_maker() as session:
            statement = insert(Message).values(message=message)
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


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id}: {data}", add_to_database=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", add_to_database=False)


@router.get('/')
def get_chat_page(request: Request):
    return templates.TemplateResponse('chat.html', {"request": request})
