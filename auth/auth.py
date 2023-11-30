from fastapi import Depends
from fastapi_users import fastapi_users
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from auth.database import User

cookie_transport = CookieTransport(cookie_name="NovaNatter", cookie_max_age=3600)

SECRET = "dfsdlf213dlsfgfifdnek323xcvcvcsddsdsxnnmnm"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
