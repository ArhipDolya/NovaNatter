from fastapi import WebSocket, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from .chat_controller import ChatController


router = APIRouter(prefix="/chat", tags=['chat'])
chat_controller = ChatController()


@router.get('/last_messages')
async def get_last_messages(session: AsyncSession = Depends(get_async_session)):
    return await chat_controller.get_last_messages(session)


@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await chat_controller.websocket_endpoint(websocket, username)