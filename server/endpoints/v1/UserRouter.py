from fastapi import Depends, HTTPException, status, APIRouter,Request
from sqlalchemy.orm import Session
from crud.UserCrud import create_user_account, get_user_by_username,get_users
from schemas.TokenSchemas import TokenSchema
from schemas.UserSchemas import User, requestdetails, CreateUser
from fastapi.security import OAuth2PasswordRequestForm
from models.User import User
from models.Token import Token
from core.security import verify_password, create_access_token
from core.auth_bearer import get_current_user
from db.database import get_db
# from dotenv import load_dotenv

# import os

# load_dotenv()

router = APIRouter()


@router.post("/register/", response_model=None, tags=["Register"])
async def register(user: CreateUser, db: Session = Depends(get_db)):
    create_user = create_user_account(db=db, user=user)
    return create_user


@router.post("/token" , tags=["Auth"]  ,response_model=None)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}



# @router.get("auth/facebook/callback", tags=["auth/facebook/"] )
# def facebook_oauth2_scheme(requests:Request):
#     token_url = f"https://graph.facebook.com/v12.0/oauth/access_token?client_id={FACEBOOK_APP_ID}&redirect_uri={FACEBOOK_REDIRECT_URI}&client_secret={FACEBOOK_APP_SECRET}&code={requests}"
#     response = requests.get(token_url)
#     token_data = response.json()
#     # Get user info with the access token
#     if "access_token" in token_data:
#         user_info_url = f"https://graph.facebook.com/me?fields=id,name,email&access_token={token_data['access_token']}"
#         user_response = requests.get(user_info_url)
#         user_data = user_response.json()
#         return user_data
#     else:
#         raise HTTPException(status_code=400, detail="Failed to fetch user data")
    
   


# @router.get('auth/github/callback',tags=["auth/github"])
# def github_oauth2_scheme(requests:Request):
#     code = requests.query_params['code']
    



@router.get("/users/", response_model=None, tags=["User"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    users = get_users(db, skip=skip, limit=limit)
    return users    