import re

from loguru import logger
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, models, schemas
from fastapi_users import exceptions as user_exceptions

from database import User, get_user_db
from .tasks import send_registration_email

from config import SECRET_KEY


logger.add("logs.log", rotation="500 MB", level="INFO")

SECRET = SECRET_KEY


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {user.id} has registered.")
        send_registration_email.delay(user.email)

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:

        if not self.is_valid_email(user_create.email):
            raise user_exceptions.UserAlreadyExists()
        
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise user_exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return bool(re.match(email_pattern, email))


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


