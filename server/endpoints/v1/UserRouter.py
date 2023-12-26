from fastapi import Depends, HTTPException, status, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from crud.UserCrud import create_user_account, get_user_by_username,get_users
from schemas.TokenSchemas import TokenSchema
from schemas.UserSchemas import User, requestdetails, CreateUser, userResponse, UserInDB
from fastapi.security import OAuth2PasswordRequestForm
from models.User import User
from models.Token import Token
from core.security import verify_password, create_access_token, create_refresh_token, get_password_hash
from core.auth_bearer import get_current_user
from db.database import get_db


router = APIRouter()


@router.post("/register/", response_model=None, tags=["Register"])
async def register(user: CreateUser, db: Session = Depends(get_db)):
    create_user = create_user_account(db=db, user=user)
    return create_user


@router.post("/token")
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


@router.get("/users/", response_model=None, tags=["User"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    users = get_users(db, skip=skip, limit=limit)
    return users
