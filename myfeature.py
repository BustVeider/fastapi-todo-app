from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import TaskModel, UserModel
from security import get_password_hash
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Todo-api with PostgreSQL")

class TaskSchema(BaseModel):
    title: str
class UserCreateSchema(BaseModel):
    username: str
    password: str


@app.get("/tasks", tags=["Task"])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).all()
    return {"tasks": tasks}

@app.post("/tasks", tags=["Task"])
def add_task(task: TaskSchema, db:Session = Depends(get_db)):
    new_task = TaskModel(title=task.title)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message" : "Task added successfully", "task": new_task}

@app.delete("/tasks/{task_id}", tags=["Task"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if db_task is None:
        raise  HTTPException(status_code=404, detail="Task not foud")
    db.delete(db_task)
    db.commit()
    return  {"message" : f"Task with ID {task_id} deleted"}

@app.patch("/tasks/{task_id}", tags=["Task"])
def status_update(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if db_task is None:
        raise  HTTPException(status_code=404, detail="Task not foud")
    db_task.is_completed = True
    db.commit()
    return  {"message" : f"Task {task_id} status updated"}

@app.patch("/register", tags=["Auth"])
def register_user(user: UserCreateSchema, db: Session= Depends(get_db)):
    hashed_pwd = get_password_hash(user.password)
    new_user = UserModel(username = user.username, hashed_password = hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registreted successfully", "username": new_user.username}