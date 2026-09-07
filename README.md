# Multi-User Todo API with Database Migrations

A secure, multi-user production-ready backend service for managing tasks, built with modern Python frameworks and PostgreSQL.

## Tech Stack
- **Backend Framework:** FastAPI (Python)
- **Data Validation:** Pydantic v2
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Security & Auth:** JWT (JSON Web Tokens), OAuth2 (Password Bearer), Bcrypt password hashing
- **Database Migrations:** Alembic

## Project Evolution
- **v1.0.0 (JSON-based):** Basic task persistence using local JSON files.
- **v2.0.0 (SQLite Integration):** Upgraded to a relational database for precise deletion using unique auto-increment IDs.
- **v3.0.0 (PostgreSQL Migration):** Migrated to a production-ready PostgreSQL database using SQLAlchemy ORM.
- **v4.0.0 (Security & Multi-User):** Implemented database relationships (One-to-Many). Added secure user registration with Bcrypt hashing and fully protected endpoints via OAuth2 JWT bearer tokens.
- **v5.0.0 (Database Migrations):** Integrated Alembic to handle schema modifications gracefully without database loss.

## Core Features
- User registration with one-way password hashing.
- Standard OAuth2 login endpoint returning JWT access tokens.
- Automatic user identity resolution from JWT payloads (no manual user ID entry required).
- Full CRUD operations for tasks linked specifically to the authenticated user.
- Complete tracking of schema updates through Alembic migration scripts.

## Installation & Running
1. Clone the repository.
2. Install required packages:
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary bcrypt pyjwt alembic
   ```
3. Set your PostgreSQL credentials in `database.py` and `alembic.ini`.
4. Run database migrations:
   ```bash
   alembic upgrade head
   ```
5. Start the local server:
   ```bash
   fastapi dev myfeature.py
   ```
6. Explore full interactive API documentation at: `http://127.0.0`

