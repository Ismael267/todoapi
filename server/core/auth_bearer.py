from jose import jwt
from fastapi import Request, HTTPException, Depends, status 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from schemas.UserSchemas import UserResponse
from core.settings import settings



REFRESH_TOKEN_EXPIRE_MINUTES =settings.REFRESH_TOKEN_EXPIRE_MINUTES
ALGORITHM =settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES=settings.ACCESS_TOKEN_EXPIRE_MINUTES
JWT_SECRET_KEY=settings.JWT_REFRESH_SECRET_KEY
JWT_REFRESH_SECRET_KEY=settings.JWT_REFRESH_SECRET_KEY

# secure= HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decodeJWT(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user 
    

def decodeJWT(jwtoken:str):
    try :
        payload= jwt.decode(jwtoken,JWT_SECRET_KEY,ALGORITHM)
        return payload
    except InvalidTokenError:
        return None
# class JWTBearer(HTTPBearer):
#     def __init__(self, auto_error: bool = True):
#         super(JWTBearer, self).__init__(auto_error=auto_error)

#     async def __call__(self, request: Request):
#         credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
#         if credentials:
#             if not credentials.scheme == "Bearer":
#                 raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
#             if not self.verify_jwt(credentials.credentials):
#                 raise HTTPException(status_code=403, detail="Invalid token or expired token.")
#             return credentials.credentials
#         else:
#             raise HTTPException(status_code=403, detail="Invalid authorization code.")
#     def verify_jwt(self, jwtoken: str) -> bool:
#         isTokenValid: bool = False
#         try:
#             payload = decodeJWT(jwtoken)
#         except:
#             payload = None
#         if payload:
#             isTokenValid = True
#         return isTokenValid
# jwt_bearer = JWTBearer()    