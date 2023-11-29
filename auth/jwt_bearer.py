from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth.jwt_handler import decode_jwt_token


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code=403, detail='Invalid or Expired Token')
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Token has expired")
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid or Expired Token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def verify_jwt(self, jwtoken: str):
        is_token_valid: bool = False
        payload = decode_jwt_token(jwtoken)
        if payload:
            is_token_valid = True

        return is_token_valid
