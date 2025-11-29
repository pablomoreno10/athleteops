from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Task, HealthLog, Budget, Transactions
from datetime import date

router = APIRouter(tags=["dashboard"])
templates = Jinja2Templates(directory="app/templates")

DEFAULT_USER_ID = 1

@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    tasks = (
        db.query(Task)
        .filter_by(user_id=DEFAULT_USER_ID)
        .order_by(Task.due_at.asc())
        .all()
    )

    today = date.today()
    health_log = (
        db.query(HealthLog)
        .filter_by(user_id=DEFAULT_USER_ID, date=today)
        .one_or_none()
    )

    budgets = (
        db.query(Budget)
        .filter_by(user_id=DEFAULT_USER_ID)
        .all()
    )

    
    transactions = (
        db.query(Transactions)
        .filter_by(user_id=DEFAULT_USER_ID)
        .order_by(Transactions.date.desc())
        .limit(5)
        .all()
    )


    return templates.TemplateResponse("dashboard.html",
        {
            "request": request,
            "tasks": tasks,
            "health_log": health_log,
            "budgets": budgets,
            "transactions": transactions,
            }
    )

