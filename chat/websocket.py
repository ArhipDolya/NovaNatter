from fastapi import WebSocket

from .services import add_message_to_database

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
            await add_message_to_database(message, username)
        for connection in self.active_connections:
            websocket = self.active_connections[connection]
            await websocket.send_text(message)