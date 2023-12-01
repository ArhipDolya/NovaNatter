from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from services.item_service import create_item, get_items
from database import get_db

router = APIRouter()


@router.post('/create-item')
async def create_item(name: str, description: str, db: Session = Depends(get_db)):
    return create_item(db, name=name, description=description)


@router.get('/get_items')
async def get_items_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_items(db, skip=skip, limit=limit)
