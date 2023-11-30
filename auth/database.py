from datetime import datetime
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, TIMESTAMP, Boolean, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from config import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD


DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"
Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String(length=1024), nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_active = Column(Boolean, default=True, nullable=True)
    is_superuser = Column(Boolean, default=False, nullable=True)
    is_verified = Column(Boolean, default=False, nullable=True)


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
