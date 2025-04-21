from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
from app.deps import get_current_user
from app.models import User

router = APIRouter()

# ROTAS PÚBLICAS
@router.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)

@router.post("/users/{user_id}/tasks/", response_model=schemas.Task)
def create_task_for_user(user_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task, user_id=user_id)

# ROTAS PRIVADAS - USUÁRIO AUTENTICADO
@router.get("/tasks/me/", response_model=list[schemas.Task])
def get_my_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(crud.models.Task).filter(crud.models.Task.owner_id == current_user.id).all()

@router.post("/tasks/me/", response_model=schemas.Task)
def create_my_task(task: schemas.TaskCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task, user_id=current_user.id)
