import os
from fastapi import UploadFile, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_async_session, get_db
from .models import User

UPLOAD_DIR = 'images'


async def save_uploaded_file(file: UploadFile, user: User, db: Session = Depends(get_async_session)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"{user.username}_{file.filename}"

    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(file_path, 'wb') as buffer:
            buffer.write(file.file.read())

        user.profile_image = filename
        await db.commit()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}",
        )

    return {'filename': filename}