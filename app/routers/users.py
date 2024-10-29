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
