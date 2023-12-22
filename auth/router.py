from fastapi import APIRouter, Depends, File, UploadFile

from database import User, get_async_session
from dependencies.auth_dependency import current_user, fastapi_users
from .upload_image import save_uploaded_file

from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()


@router.get('/status')
async def get_authentication_status(user: User = Depends(current_user)):
    return {"is_authenticated": current_user is not None}


@router.get('/me')
async def get_current_user(user: User = Depends(current_user)):
    return user


@router.post('/uploadfile')
async def create_upload_file(file: UploadFile = File(...), user: User = Depends(current_user), db: Session = Depends(get_async_session)):
    return await save_uploaded_file(file, user, db)

