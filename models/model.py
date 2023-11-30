from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from pydantic import BaseModel, Field, EmailStr

from database import Base


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)