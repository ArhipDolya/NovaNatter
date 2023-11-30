from sqlalchemy.orm import Session
from models.model import Item


def create_item(db: Session, name: str, description: str):
    db_item = Item(name=name, description=description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Item).offset(skip).limit(limit).all()


