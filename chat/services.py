from sqlalchemy import insert
from database import async_session_maker

from chat.models import Message


async def add_message_to_database(message: str, username: str):
    async with async_session_maker() as session:
        statement = insert(Message).values(message=message, username=username)
        await session.execute(statement)
        await session.commit()

