from fastapi import APIRouter, Depends, HTTPException, status
from app.models import User
from app.schemas import UserBase, UserCreate, UserLogin, AuthResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.db import get_db
from app.auth import check_password, hash_password, create_access_token

router = APIRouter(prefix="/auth", tags=["/auth"])

#register route with JSON response
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

@router.post("/login", response_model = AuthResponse)
def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_login.email).first()
    if user:
        if not check_password(user_login.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password does not match our records"
            )
        else:
            token = create_access_token({"sub": user.email})
            return {"access_token": token, "token_type": "bearer"}

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with that email does not exist"
        )