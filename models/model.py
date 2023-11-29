from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, Field, EmailStr

from database import Base


class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(default=None)
    content: str = Field(default=None)

    class Config:
        schema_extra = {
            "post": {
                "title": "Some title",
                "content": "Some content"
            }
        }


class UserSchema(BaseModel):
    username: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password1: str = Field(default=None)
    password12: str = Field(default=None)

    class Config:
        schema_extra = {
            "user": {
                "username": "user",
                "email": "user@gmail.com",
                "password1": "user1234",
                "password2": "user1234",
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(default=None)
    password1: str = Field(default=None)

    class Config:
        schema_extra = {
            "user": {
                "email": "user@gmail.com",
                "password1": "user1234",
            }
        }


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)