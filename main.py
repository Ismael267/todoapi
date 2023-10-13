from fastapi import Depends, FastAPI
from fastapi import Depends, FastAPI, HTTPException,status
from sqlalchemy.orm import Session
from todoapi import crud, schemas, models
from database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime,timedelta 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Fonction de dépendance pour obtenir une session de base de données
origins = [
  
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def add_one_day_to_date(iso8601_date):
    try:
        date_obj = datetime.fromisoformat(iso8601_date)
        updated_date = date_obj + timedelta(days=1)
        updated_iso8601_date = updated_date.isoformat()
        return updated_iso8601_date
    except ValueError:
        raise ValueError("La date ISO 8601 n'est pas valide")

# Endpoints pour les utilisateurs

@app.post("/user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# Endpoints pour les tâches

@app.post("/task/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)


@app.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


@app.delete("/delete/task/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.delete_task(db, task_id)
    return task


@app.put('/update/task/{task_id}', response_model=schemas.Task)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tâche non trouvée")

    updated_task = crud.update_task(db, task_id, task_update)
    return updated_task


@app.put('/update/taskDate/{task_id}',response_model=schemas.Task)
def update_taskDate(task_id:int, task_updateDate:schemas.TaskDateUpdate, db:Session=Depends(get_db) ):
    db_task=crud.get_task(db,task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Tache non trouver')
    updated_taskDate=crud.update_task(db,task_id,task_updateDate)
    return updated_taskDate
    

@app.put('/update/taskDatePlus/{task_id}', response_model=schemas.Task)
def update_taskDate(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id)
    
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tache non trouvée')
    
    # Ajoute un jour à la date de réalisation
    updated_data = {"dateOfRealisation": add_one_day_to_date(db_task.dateOfRealisation)}
    updated_task = crud.updateByOneDay(db, task_id, updated_data)
    
    return updated_task
