from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    username: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password1: str = Field(default=None)
    password2: str = Field(default=None)

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