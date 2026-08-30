from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI(title="Todo-api")
FILE_NAME = "todo_list.json"

class Task(BaseModel):
    title: str

def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)

@app.get("/tasks", tags=["Look a tasks"])
def get_tasks():
    to_do_list = load_tasks()
    return {"tasks": to_do_list}

@app.post("/tasks", tags=["Add tasks"])
def add_task(task: Task):
    to_do_list = load_tasks()
    to_do_list.append(task.title)
    save_tasks(to_do_list)
    return {"message" : "Task added successfuly", "task": task.title}

@app.delete("/tasks/{task_index}", tags=["Delete task"])
def delete_task(task_index: int):
    to_do_list = load_tasks()

    if 0<=task_index<len(to_do_list):
        removed = to_do_list.pop(task_index)
        save_tasks(to_do_list)
        return {"message": f"Task '{removed}' delete successfully"}

    raise HTTPException(status_code=404, detail="Task not found")
