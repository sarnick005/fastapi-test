from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from . import models
from . import schemas
from .database import engine, get_db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="FastAPI MySQL Example")

# Create database tables
try:
    models.Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating database tables: {e}")
    raise


@app.post(
    "/users/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = models.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        )


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        )


@app.get("/users/", response_model=list[schemas.UserResponse])
async def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        users = db.query(models.User).offset(skip).limit(limit).all()
        return users
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        )
