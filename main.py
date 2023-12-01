import uvicorn

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users import FastAPIUsers

from sqlalchemy.orm import Session

from database import SessionLocal, User
from controllers import auth_controller

from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate


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


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.post('/create-item')
async def create_item(name: str, description: str, db: Session = Depends(get_db)):
    return auth_controller.create_item(db, name=name, description=description)


@app.get('/get_items')
async def get_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user: User = Depends(current_user)):
    return auth_controller.get_items(db, skip=skip, limit=limit)



if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
