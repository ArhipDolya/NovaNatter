from fastapi import APIRouter, Depends

from database import User
from dependencies.auth_dependency import current_user, fastapi_users

from controllers.auth_controller import protected_route


router = APIRouter()


@router.get("/protected-route")
async def protected_route(user: User = Depends(current_user)):
    return protected_route(user)