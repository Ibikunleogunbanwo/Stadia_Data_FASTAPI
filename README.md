🏟️ Stadium Directory API

A FastAPI-based RESTful API for managing stadium information with full CRUD functionality.

## 🚀 Features

- **Full CRUD Operations** - Create, Read, Update, and Delete stadium records
- **Flexible Search** - Find stadiums by ID or name (case-insensitive)
- **SQLite Backend** - Lightweight database with automatic initialization
- **Data Validation** - Robust input validation using Pydantic models

## 📋 API Endpoints

| Method | Endpoint                      | Description                     | Status Codes   |
|--------|-------------------------------|---------------------------------|----------------|
| `POST`   | `/create_stadium/`            | Create new stadium              | 201, 400       |
| `GET`    | `/stadiums/`                  | List all stadiums               | 200            |
| `GET`    | `/stadium/{stadium_id}`       | Get stadium by ID               | 200, 404       |
| `GET`    | `/stadium_name/{stadium_name}`| Get stadium by name             | 200, 404       |
| `PUT`    | `/stadium_by_id/{stadium_id}` | Update stadium by ID            | 200, 404       |
| `DELETE` | `/stadium/{stadium_id}`       | Delete stadium by ID            | 204, 400       |

## 🏗️ Stadium Model Structure

```python
class Stadium(BaseModel):
    id: int | None = None  # Auto-generated
    name: str              # Required, unique
    city: str              # Required
    capacity: int          # Required
    club: str | None = None # Optional
    open_year: int         # Required


⚙️ Setup & Installation

Clone the repository

bash
git clone https://github.com/yourusername/stadium-api.git
cd stadium-api
Install dependencies

bash
pip install fastapi uvicorn sqlite3 pydantic
Run the application

bash
uvicorn main:app --reload
Access the API at http://localhost:8000



🔍 Testing the API
Test using:

curl commands

Postman/Insomnia

Interactive Swagger UI at http://localhost:8000/docs

Redoc documentation at http://localhost:8000/redoc


Example Requests
Create a new stadium:

bash
curl -X POST "http://localhost:8000/create_stadium/" \
-H "Content-Type: application/json" \
-d '{"name":"Camp Nou","city":"Barcelona","capacity":99354,"club":"FC Barcelona","open_year":1957}'
Get all stadiums:


bash
curl "http://localhost:8000/stadiums/"


💾 Database
Automatically creates stadiums.db with this schema:

sql
CREATE TABLE stadia(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    city TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    club TEXT,
    open_year INTEGER NOT NULL
)


📜 License
MIT License - See LICENSE for details
