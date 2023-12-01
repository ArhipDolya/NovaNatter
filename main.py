import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.auth import auth_backend
from auth.schemas import UserRead, UserCreate
from auth import router

from routers import item_router


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


app.include_router(
    router.fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    router.fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(item_router.router, prefix='/items', tags=["items"])


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
