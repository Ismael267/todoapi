from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr

class ResponseBase(BaseModel):
    
    email:EmailStr
    username:str

class ResponseCreate(ResponseBase):
    email:EmailStr
    username:str

