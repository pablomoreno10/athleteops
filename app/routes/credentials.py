from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.models import User
from app.schemas import UserBase, UserCreate, UserLogin, AuthResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from app.db import get_db
from app.auth import check_password, hash_password, create_access_token

router = APIRouter(prefix="/auth", tags=["/auth"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    """Display login page."""
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    """Display register page."""
    return templates.TemplateResponse("register.html", {"request": request})

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

@router.post("/register/form")
def create_user_from_form(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Register user from form submission."""
    user_exists = db.query(User).filter(User.email == email).first()
    if user_exists:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Email already registered"},
            status_code=400
        )

    hashed_pword = hash_password(password)
    new_user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        hashed_password=hashed_pword,
        created_at=datetime.now(timezone.utc),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Auto-login after registration
    token = create_access_token(
        {"sub": new_user.email, "user_id": new_user.id},
        expires_delta=timedelta(minutes=15)
    )
    
    response = RedirectResponse("/", status_code=303)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=15 * 60,
    )
    return response

@router.post("/login", response_model = AuthResponse)
def login_user(user_login: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_login.email).first()
    if user:
        if not check_password(user_login.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password does not match our records"
            )
        else:
            # Create token with user_id included
            token = create_access_token(
                {"sub": user.email, "user_id": user.id},
                expires_delta=timedelta(minutes=15)
            )
            
            # Set HttpOnly cookie for web requests
            response.set_cookie(
                key="access_token",
                value=token,
                httponly=True,
                samesite="lax",
                secure=False,  # Set to True in production with HTTPS
                max_age=15 * 60,  # 15 minutes
            )
            
            # Return JSON response for API clients (backward compatible)
            return {"access_token": token, "token_type": "bearer"}

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with that email does not exist"
        )

@router.post("/login/form")
def login_user_from_form(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Login user from form submission."""
    user = db.query(User).filter(User.email == email).first()
    if user:
        if not check_password(password, user.hashed_password):
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "error": "Password does not match our records"},
                status_code=401
            )
        else:
            token = create_access_token(
                {"sub": user.email, "user_id": user.id},
                expires_delta=timedelta(minutes=15)
            )
            
            response = RedirectResponse("/", status_code=303)
            response.set_cookie(
                key="access_token",
                value=token,
                httponly=True,
                samesite="lax",
                secure=False,
                max_age=15 * 60,
            )
            return response
    else:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "User with that email does not exist"},
            status_code=401
        )

@router.post("/logout")
def logout_user(response: Response):
    """Logout user by clearing the authentication cookie."""
    response.delete_cookie(key="access_token", httponly=True, samesite="lax")
    return {"message": "Successfully logged out"}

@router.post("/logout/form")
def logout_user_from_form():
    """Logout user from form submission (redirects to login)."""
    response = RedirectResponse("/auth/login", status_code=303)
    response.delete_cookie(key="access_token", httponly=True, samesite="lax")
    return response