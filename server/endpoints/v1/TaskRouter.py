from fastapi import Depends, HTTPException,status ,APIRouter
from sqlalchemy.orm import Session
from crud.TaskCrud import create_task,get_tasks,delete_task,get_task,update_task,updateByOneDay,add_one_day_to_date
from schemas.TaskSchemas import TaskList,TaskDateUpdate,TaskUpdate,TaskCreate
from core.auth_bearer import JWTBearer
from db.database import get_db



router= APIRouter(
    tags=["Task"] 
)


@router.post("/task/", response_model=TaskList )
def create_one_task(task: TaskCreate, db: Session = Depends(get_db) ,dependencies=Depends(JWTBearer())):
    return create_task(db=db, task=task)


@router.get("/tasks/", response_model=list[TaskList])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db) ,dependencies=Depends(JWTBearer())):
    tasks = get_tasks(db, skip=skip, limit=limit)
    return tasks


@router.delete("/delete/task/{task_id}", response_model=TaskList )
def delete_task(task_id: int, db: Session = Depends(get_db), dependencies= Depends(JWTBearer())):
    task = delete_task(db, task_id)
    return task


@router.put('/update/task/{task_id}', response_model=TaskList )
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db), dependencies= Depends(JWTBearer())):
    db_task = get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tâche non trouvée")
    updated_task = update_task(db, task_id, task_update)
    return updated_task


@router.put('/update/taskDate/{task_id}',response_model=TaskList)
def update_taskDate(task_id:int, task_updateDate:TaskDateUpdate, db:Session=Depends(get_db), dependencies =Depends(JWTBearer()) ):
    db_task=get_task(db,task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Tache non trouvée')
    updated_taskDate=update_task(db,task_id,task_updateDate)
    return updated_taskDate
    

@router.put('/update/taskDatePlus/{task_id}', response_model=TaskList,tags=["Task"])
def update_taskDate(task_id: int, db: Session = Depends(get_db), dependencies =Depends(JWTBearer())):
    db_task = get_task(db, task_id) 
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tache non trouvée') 
    # Ajoute un jour à la date de réalisation
    updated_data = {"dateOfRealisation": add_one_day_to_date(db_task.dateOfRealisation)}
    updated_task =updateByOneDay(db, task_id, updated_data)
    return updated_task
