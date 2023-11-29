import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from controllers import auth

app = FastAPI(title='NovaNatter')


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


@app.post('/create-item')
async def create_item(name: str, description: str, db: Session = Depends(get_db)):
    return auth.create_item(db, name=name, description=description)


@app.get('/get_items')
async def get_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return auth.get_items(db, skip=skip, limit=limit)


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
