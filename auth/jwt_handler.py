import time
import jwt
from jwt import PyJWTError
from fastapi import HTTPException, status
from config import JWT_SECRET, JWT_ALGORITHM


def token_response(token: str, token_type: str = "bearer", expires_in: int = 600):
    return {
        "access_token": token,
        "token_type": token_type,
        "expires_in": expires_in,
    }


def sign_JWT(userID: str, expires_in: int = 600):
    payload = {
        'userID': userID,
        'expires': time.time() + expires_in
    }
    token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return token_response(token, expires_in=expires_in)


def decode_jwt_token(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        if decoded_token['expires'] < time.time():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        return decoded_token
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
