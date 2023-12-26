from jose import jwt
from fastapi import Request, HTTPException, Depends, status 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from schemas.UserSchemas import userResponse
# from db.database import get_db

REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_SECRET_KEY="1d08056cb3fe4f19a9c9d12a0d4553a5f6aa78f3c18246ca06fe5a907576d170"
JWT_REFRESH_SECRET_KEY="bed8404726628eb136ff0f85c7257ce20800e303db9574aabc5ab123f83aeb5f"

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