from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from datetime import datetime,timedelta 
import re


def is_valid_iso8601_date(date_str):
    try:
        datetime.fromisoformat(date_str)
        return True
    except ValueError:
        return False

def add_one_day_to_date(iso8601_date):
    try:
        # date_obj = datetime.fromisoformat(iso8601_date)
        updated_date = date_obj + timedelta(days=0.5)
        updated_iso8601_date = updated_date.isoformat()
        return updated_iso8601_date
    except ValueError:
        raise ValueError("La date ISO 8601 n'est pas valide")



def create_user(db: Session, user: schemas.UserCreate):
    """
    Crée un nouvel utilisateur dans la base de données.
    """
    fake_hashed_password = user.hashed_password + "notreallyhashed"
    db_user = models.User(
        email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Récupère une liste d'utilisateurs depuis la base de données.
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    """
    Récupère un utilisateur par son adresse e-mail depuis la base de données.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_task(db, task_id):
    """
    Récupère une tâche à partir de la base de données par son ID.
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    return db_task


def create_task(db: Session, task: schemas.TaskCreate):
    """
    Crée une nouvelle tâche dans la base de données.
    """
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    """
    Récupère une liste de tâches depuis la base de données.
    """
    return db.query(models.Task).offset(skip).limit(limit).all()


def update_task(db, task_id, updated_data):
    """
    Met à jour l'etat  d'une tâche dans la base de données.
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="La tâche n'existe pas")

    for key, value in updated_data.dict().items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def update_taskdate(db, task_id, updated_data):
    """
    Met à jour la date d'une tâche dans la base de données.
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="La tâche n'existe pas")

    for key, value in updated_data.dict().items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def updateByOneDay(db, task_id, updated_data):
    """
    Met à jour la date  d'une tâche d'un jour dans la base de données.
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="La tâche n'existe pas")

    for key, value in updated_data.items():
        if key == "dateOfRealisation":
            if is_valid_iso8601_date(value):
               
                updated_date = add_one_day_to_date(value)
                setattr(db_task, key, updated_date)
            else:
                raise HTTPException(status_code=404, detail="La date de réalisation n'est pas au format ISO 8601")
        else:
            setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    """
    Supprime une tâche de la base de données.
    """
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    print(db_task)
    if not db_task:
        raise HTTPException(status_code=404, detail="La tâche n'existe pas")
    db.delete(db_task)
    db.commit()
    return db_task


#fonction de filtre et utilitaire

