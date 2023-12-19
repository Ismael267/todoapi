from fastapi import Depends, HTTPException,status ,APIRouter
from sqlalchemy.orm import Session
from crud.UserCrud import create_user_account,get_users
from schemas.TokenSchemas import TokenSchema
from schemas.UserSchemas import User,requestdetails,CreateUser
from models.User import User
from models.Token import Token
from core.security import verify_password,create_access_token,create_refresh_token
from core.auth_bearer import JWTBearer
from db.database import get_db



router = APIRouter()


@router.post("/register/", response_model=None,tags=["Register"])
async def register(user: CreateUser, db: Session = Depends(get_db) ):
    create_user = create_user_account(db=db, user=user)
    return create_user

@router.post('/login' ,response_model=TokenSchema ,tags=["Auth"])
async def login(request: requestdetails, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    hashed_pass = user.hashed_password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        ) 
    access=create_access_token(user.id)
    refresh = create_refresh_token(user.id)
    token_db = Token(user_id=user.id,  access_token=access,  refresh_token=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {
        "access_token": access,
        "refresh_token": refresh,
    }
    #

@router.get("/users/", response_model=None ,tags=["User"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),dependencies=Depends(JWTBearer())):
    users = get_users(db, skip=skip, limit=limit)
    return users