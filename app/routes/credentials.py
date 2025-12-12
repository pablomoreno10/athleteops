from fastapi import APIRouter, Depends, HTTPException, status
from app.models import User
from app.schemas import UserBase, UserCreate
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.db import get_db
from app.auth import check_password, hash_password

router = APIRouter(prefix="/auth", tags=["/auth"])

@router.post("/register", response_model=UserBase)
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.email == user_create.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_pword = hash_password(user_create.password)
    new_user = User(
        email=user_create.email,
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        hashed_password=hashed_pword,
        created_at=datetime.now(timezone.utc),
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
