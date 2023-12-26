from sqlalchemy.orm import Session
from models.User import User
from fastapi import HTTPException
from core.security import get_password_hash,verify_password



def create_user_account(db: Session, user):
    existing_user = db.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password =get_password_hash(user.hashed_password)

    new_user = User(username=user.username, email=user.email, hashed_password=encrypted_password )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Récupère une liste d'utilisateurs depuis la base de données.
    """
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    """
    Récupère un utilisateur par son adresse e-mail depuis la base de données.
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    """
    Récupère un utilisateur par son username depuis la base de données.
    """
    return db.query(User).filter(User.username == username).first()


def get_token(data,db):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email is not verify with us",
            headers="www-authenticate:bearer"
        )
    if not verify_password(data.password,user.password) :
        raise HTTPException(
            status_code=400,
            detail="Password incorrect",
            headers="www-authenticate:bearer"
            )
    _verify_user_access(user=user)
    return '' #return acces token et refresh token     
    
def _verify_user_access(user:User):
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Account has been disabled by admin.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Your account email is not verified yet.",
            headers={"WWW-Authenticate": "Bearer"},
        )    
        
        