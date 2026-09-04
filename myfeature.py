from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import TaskModel, UserModel
from security import get_password_hash, verify_password, create_access_token, get_user_id_from_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Todo-api with PostgreSQL")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class TaskSchema(BaseModel):
    title: str
class UserCreateSchema(BaseModel):
    username: str
    password: str
def get_currect_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = get_user_id_from_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Cloud not validate credentials")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.get("/tasks", tags=["Task"])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).all()
    return {"tasks": tasks}

@app.post("/tasks", tags=["Task"])
def add_task(task: TaskSchema, db:Session = Depends(get_db), current_user: UserModel = Depends(get_currect_user)):
    new_task = TaskModel(title=task.title, user_id = current_user.id)
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

@app.post("/login", tags = ["Auth"])
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if db_user is None or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=404, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token , "token_type": "bearer"}