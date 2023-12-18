from fastapi import APIRouter, Depends

from database import User
from dependencies.auth_dependency import current_user, fastapi_users

router = APIRouter()


@router.get('/status')
async def get_authentication_status(user: User = Depends(current_user)):
    return {"is_authenticated": current_user is not None}


@router.get('/me')
async def get_current_user(user: User = Depends(current_user)):
    return user
