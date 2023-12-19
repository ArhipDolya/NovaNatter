from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from config import SECRET_KEY


SHORT_TOKEN_LIFETIME_SECONDS = 3600  # one hour
LONG_TOKEN_LIFETIME_SECONDS = 30 * 24 * 3600  # 30 days

cookie_transport = CookieTransport(cookie_name="NovaNatter", cookie_max_age=3600)

SECRET = "fjskjdkfffffdsvnfdjbhsbdjsknfdvjfdsdnkfjdsjdjvjdsnjdjs"


def get_jwt_strategy(remember_me: bool = False) -> JWTStrategy:
    lifetime_seconds = LONG_TOKEN_LIFETIME_SECONDS if remember_me else SHORT_TOKEN_LIFETIME_SECONDS
    return JWTStrategy(secret=SECRET, lifetime_seconds=lifetime_seconds)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
