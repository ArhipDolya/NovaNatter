import uvicorn

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from database import SessionLocal
from controllers import auth
from schemas.UserSchema import UserSchema, UserLoginSchema
from services.UserService import UserService

from auth.jwt_handler import sign_JWT


app = FastAPI(title='NovaNatter')


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.post('/register', tags=['user'])
async def register(user: UserSchema, db: Session = Depends(get_db)):
    db_user = UserService.create_user(db, user)
    token = sign_JWT(db_user.id)

    return token


@app.post('/login', tags=['user'])
async def login_user(user: UserLoginSchema, db: Session = Depends(get_db)):
    return UserService.login_user(db, user)


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
