Here's a Markdown guide on integrating MySQL with FastAPI while keeping credentials secure in a `.env` file.

---

# Using MySQL with FastAPI

This guide walks you through setting up MySQL with FastAPI using `SQLAlchemy` for database ORM and managing sensitive credentials securely with a `.env` file.

## Requirements

Ensure you have the following dependencies installed:

```bash
pip install fastapi uvicorn sqlalchemy pymysql python-dotenv
```

- **`fastapi`** - The FastAPI framework.
- **`uvicorn`** - ASGI server for FastAPI.
- **`sqlalchemy`** - ORM for database interactions.
- **`pymysql`** - MySQL database driver.
- **`python-dotenv`** - To load environment variables from `.env` files.

## Project Structure

```plaintext
.
├── app
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry point
│   ├── database.py             # Database connection setup
│   ├── models.py               # SQLAlchemy models
│   ├── routers                 # API routers
│   └── .env                    # Environment variables
└── requirements.txt            # Required packages
```

## Steps

### Step 1: Create `.env` File

Create a `.env` file in the root directory to store sensitive information like MySQL credentials.

```plaintext
# .env
DB_USER=<your_mysql_username>
DB_PASSWORD=<your_mysql_password>
DB_HOST=localhost
DB_PORT=3306
DB_NAME=<your_database_name>
```

> **Note**: Replace `<your_mysql_username>`, `<your_mysql_password>`, and `<your_database_name>` with your actual MySQL credentials.

### Step 2: Configure Database Connection in `database.py`

Create a `database.py` file to manage the database connection and session.

```python
# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database credentials from .env
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Step 3: Define Models in `models.py`

Define your SQLAlchemy models (tables) in `models.py`. Here’s an example model for a `User` table.

```python
# app/models.py
from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    email = Column(String(50), unique=True, index=True)
    age = Column(Integer)
```

### Step 4: Integrate Routes in `main.py`

In `main.py`, include the FastAPI setup, database initialization, and router inclusion.

```python
# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .routers import users

app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(users.router)
```

### Step 5: Create a Router (`routers/users.py`)

Add a router to handle user-related endpoints using database sessions.

```python
# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/")
async def create_user(name: str, email: str, age: int, db: Session = Depends(get_db)):
    db_user = models.User(name=name, email=email, age=age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Step 6: Run the Application

To start the FastAPI server, use:

```bash
uvicorn app.main:app --reload
```

## Summary

This setup enables secure MySQL integration with FastAPI. Sensitive credentials are stored in a `.env` file, which is loaded with `python-dotenv` to maintain security. SQLAlchemy ORM models and dependency injections are used to manage database interactions seamlessly.