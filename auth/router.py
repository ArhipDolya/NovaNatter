from fastapi import APIRouter, Depends

from database import User
from dependencies.auth_dependency import current_user, fastapi_users

from controllers.auth_controller import protected_route


router = APIRouter()


def pagination_params(limit: int = 10, skip: int = 0):
    return {"limit": limit, skip: skip}


@router.get("/protected-route")
async def protected_route(user: User = Depends(current_user)):
    return {"message": "This is a protected route", "user_id": user.id}


@router.get('/get_params')
async def func(params: dict = Depends(pagination_params)):
    return params


