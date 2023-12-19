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
        orm_mode = True

class requestdetails(BaseModel):
    email:EmailStr
    password:str