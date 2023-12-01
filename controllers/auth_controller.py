from fastapi import Depends
from auth.models import User
from dependencies.auth_dependency import current_user


def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"