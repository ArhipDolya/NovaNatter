from fastapi import Request, HTTPException, Depends, Response
from fastapi_users.authentication import JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase

from dependencies.auth_dependency import current_user
from database import User, get_async_session
from config import SECRET_KEY


jwt_authentication = JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)


async def check_jwt_token(request: Request = Depends()):
    """
    Middleware to check the JWT token on each request and refresh it if needed.
    """
    current_user_instance = await current_user(request)
    try:
        # Check if the token needs to be refreshed
        await jwt_authentication.get_login_response(current_user_instance, request)
    except HTTPException:
        refreshed_token = await jwt_authentication.get_login_response(
            current_user_instance, request, refresh=True
        )
        request.cookies["NovaNatter"] = refreshed_token["access_token"]