import json
from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from .websocket import ConnectionManager
from .repositories import get_last_ten_messages


class ChatController:
    def __init__(self):
        self.manager = ConnectionManager()

    async def get_last_messages(self, session: AsyncSession = Depends(get_async_session)):
        return await get_last_ten_messages(session)

    async def websocket_endpoint(self, websocket: WebSocket, username: str):
        await self.manager.connect(websocket, username)
        try:
            while True:
                data = await websocket.receive_text()
                message_data = json.loads(data)
                message_username = message_data.get('username', username)
                message = message_data.get('message', '')

                await self.manager.broadcast(f"User {message_username}: {message}", add_to_database=True, username=message_username)
        except WebSocketDisconnect:
            self.manager.disconnect(websocket, username)
            await self.manager.broadcast(f"User {username} left the chat", add_to_database=False)