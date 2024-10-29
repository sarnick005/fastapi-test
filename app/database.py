# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import pymysql
from sqlalchemy import create_engine

# Load environment variables from .env file
load_dotenv()

# Database credentials
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
print(DB_PASSWORD)

# Construct database URL with proper encoding
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost:3306/{DB_NAME}"
print(DATABASE_URL)

# Create engine with explicit parameters
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=3600,  # Recycle connections after 1 hour
    echo=False,  # Set to True for SQL query logging
)
try:
    with engine.connect() as connection:
        print(DATABASE_URL)
        print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
