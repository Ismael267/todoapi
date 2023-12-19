from fastapi import  FastAPI
from db.database import engine,Base
from fastapi.middleware.cors import CORSMiddleware
from endpoints.v1 import TaskRouter,UserRouter



Base.metadata.create_all(bind=engine)

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
app.include_router(TaskRouter.router)
app.include_router(UserRouter.router)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
        
        
# def add_one_day_to_date(iso8601_date):
#     try:
#         date_obj = datetime.fromisoformat(iso8601_date)
#         updated_date = date_obj + timedelta(days=1)
#         updated_iso8601_date = updated_date.isoformat()
#         return updated_iso8601_date
#     except ValueError:
#         raise ValueError("La date ISO 8601 n'est pas valide")

# # Endpoints pour les utilisateurs



# @app.post("/register/", response_model=None,tags=["Register"])
# async def register(user: CreateUser, db: Session = Depends(get_db) ):
#     create_user = create_user_account(db=db, user=user)
#     return create_user

# @app.post('/login' ,response_model=TokenSchema ,tags=["Auth"])
# async def login(request: requestdetails, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == request.email).first()
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
#     hashed_pass = user.hashed_password
#     if not verify_password(request.password, hashed_pass):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect password"
#         ) 
#     access=create_access_token(user.id)
#     refresh = create_refresh_token(user.id)
#     token_db = Token(user_id=user.id,  access_token=access,  refresh_token=refresh, status=True)
#     db.add(token_db)
#     db.commit()
#     db.refresh(token_db)
#     return {
#         "access_token": access,
#         "refresh_token": refresh,
#     }
#     #

# @app.get("/users/", response_model=None ,tags=["User"])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),dependencies=Depends(JWTBearer())):
#     users = get_users(db, skip=skip, limit=limit)
#     return users

# # Endpoints pour les tâches

# @app.post("/task/", response_model=TaskList ,tags=["Task"])
# def create_one_task(task: TaskCreate, db: Session = Depends(get_db) ,dependencies=Depends(JWTBearer())):
#     return create_task(db=db, task=task)


# @app.get("/tasks/", response_model=list[TaskList] ,tags=["Task"] )
# def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db) ,dependencies=Depends(JWTBearer())):
#     tasks = get_tasks(db, skip=skip, limit=limit)
#     return tasks


# @app.delete("/delete/task/{task_id}", response_model=TaskList ,tags=["Task"])
# def delete_task(task_id: int, db: Session = Depends(get_db), dependencies= Depends(JWTBearer())):
#     task = delete_task(db, task_id)
#     return task


# @app.put('/update/task/{task_id}', response_model=TaskList ,tags=["Task"])
# def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db), dependencies= Depends(JWTBearer())):
#     db_task = get_task(db, task_id)
#     if db_task is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tâche non trouvée")
#     updated_task = update_task(db, task_id, task_update)
#     return updated_task


# @app.put('/update/taskDate/{task_id}',response_model=TaskList ,tags=["Task"])
# def update_taskDate(task_id:int, task_updateDate:TaskDateUpdate, db:Session=Depends(get_db), dependencies =Depends(JWTBearer()) ):
#     db_task=get_task(db,task_id)
#     if db_task is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Tache non trouvée')
#     updated_taskDate=update_task(db,task_id,task_updateDate)
#     return updated_taskDate
    

# @app.put('/update/taskDatePlus/{task_id}', response_model=TaskList,tags=["Task"])
# def update_taskDate(task_id: int, db: Session = Depends(get_db), dependencies =Depends(JWTBearer())):
#     db_task = get_task(db, task_id) 
#     if db_task is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tache non trouvée') 
#     # Ajoute un jour à la date de réalisation
#     updated_data = {"dateOfRealisation": add_one_day_to_date(db_task.dateOfRealisation)}
#     updated_task =updateByOneDay(db, task_id, updated_data)
#     return updated_task
