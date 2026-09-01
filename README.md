# Todo API using FastAPI

This is a professional Todo web application built with Python and FastAPI. It supports adding, viewing, updating status, and deleting tasks by ID.

## Tech Stack
- **Backend:** Python, FastAPI, Pydantic
- **Database:** PostgreSQL (SQLAlchemy ORM)

## Architecture Evolution
- **v1.0.0:** Task persistence via JSON files (historical version).
- **v2.0.0:** Upgraded to relational database (SQLite) for handling deletions by unique IDs.
- **v3.0.0:** Fully migrated to a production-ready database (**PostgreSQL**) using **SQLAlchemy ORM**. Added boolean task completion statuses and `PATCH` method for status updates.

## Features
- `GET /tasks`: Retrieve all tasks with status
- `POST /tasks`: Add a new task (defaults to incomplete)
- `PATCH /tasks/{task_id}`: Mark a specific task as completed
- `DELETE /tasks/{task_id}`: Delete a task by its unique ID

## How to run
1. Clone the repository.
2. Install dependencies: `pip install fastapi uvicorn sqlalchemy psycopg2-binary`
3. Ensure PostgreSQL is running and update `DATABASE_URL` in `database.py`.
4. Run the development server: `fastapi dev myfeature.py`
5. Open interactive API docs: `http://127.0.0`
