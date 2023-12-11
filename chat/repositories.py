from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from chat.models import Message


async def get_last_ten_messages(session: AsyncSession, limit: int = 10):
    query = select(Message).order_by(Message.id.desc()).limit(limit)
    result = await session.execute(query)
    messages = result.all()
    message_list = [message[0].as_dict() for message in messages]
    return message_list

