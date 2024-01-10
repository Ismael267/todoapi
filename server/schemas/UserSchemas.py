from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr

class UserBase(BaseModel):
    email: str
    hashed_password: str


class CreateUser(UserBase):
    hashed_password: str
    email:EmailStr
    username:str


class User(BaseModel):
    id: int
    hashed_password: str
    email:EmailStr
    username:str

    class Config:
        from_attributes = True
        
class UserInDB(User):
    hashed_password:str
    username:str
    
class requestdetails(BaseModel):
    email:EmailStr
    hashed_password:str
    
class userResponse(BaseModel):
    email:EmailStr
    username:str
    