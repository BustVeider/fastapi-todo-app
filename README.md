# Todo API using FastAPI

This is a simple Todo web application built with Python and FastAPI. It supports adding, viewing, and deleting tasks by ID.

## Tech Stack
- **Backend:** Python, FastAPI, Pydantic
- **Database:** SQLite (SQL queries via `sqlite3`)

## Architecture Evolution
- **v1.0.0:** Task persistence via JSON files (historical version).
- **v2.0.0:** Upgraded to relational database (SQLite) for better data persistence and handling deletions by unique IDs.

## How to run
1. Clone the repository.
2. Install dependencies: `pip install fastapi uvicorn`
3. Run the development server: `fastapi dev myfeature.py`
4. Open interactive API docs: `http://127.0.0`
