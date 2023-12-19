from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr


class TaskBase(BaseModel):
    task: str
    completed: bool = False
    dateOfRealisation: datetime # iso 8601(%Y-%m-%d)
    dateOfExecution:datetime
      
class TaskCreate(TaskBase):
    pass


class TaskList(TaskBase):
    id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):

    completed: bool
    dateOfExecution:datetime


class TaskDelete(BaseModel):

    completed: bool


class TaskDateUpdate(BaseModel):

    dateOfRealisation: datetime
    dateOfExecution: datetime
    