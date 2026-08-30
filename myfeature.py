from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Todo-api")
conn = sqlite3.connect("todo.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL
    )
""")
conn.commit()


class Task(BaseModel):
    title: str


@app.get("/tasks", tags=["Look a tasks"])
def get_tasks():
    cursor.execute("SELECT id, title FROM tasks")
    rows = cursor.fetchall()
    to_do_list = [{"id" : row[0], "title" : row[1]} for row in rows]
    return {"tasks": to_do_list}

@app.post("/tasks", tags=["Add tasks"])
def add_task(task: Task):
    cursor.execute("INSERT INTO tasks(title) VALUES (?)", (task.title,))
    conn.commit()
    return {"message" : "Task added successfuly", "task": task.title}

@app.delete("/tasks/{task_id}", tags=["Delete a task"])
def delete_task(task_id: int):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return  {"message" : f"Task with ID {task_id} deleted"}
