from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.db import get_db
from app.enums import TaskStatus, Importance, TaskType
from app.models import Task
from app.schemas import TaskCreate, TaskRead
from app.auth import get_current_user_id

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskRead])
def list_tasks(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    tasks = db.query(Task).filter_by(user_id = user_id).order_by(Task.due_at.asc()).all()
    return tasks

@router.post("/", response_model=TaskRead)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    task = Task(
        user_id=user_id,
        status=TaskStatus.pending,
        **task_in.model_dump(),
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.post("/form")
def create_task_from_form(
    title: str = Form(...),
    course: str | None = Form(""),
    due_at: str = Form(...),
    estimated_duration_min: int = Form(...),
    importance: Importance = Form(...),
    type: TaskType = Form(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    try:
        parsed_due = datetime.fromisoformat(due_at)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid due_at format")

    if parsed_due.tzinfo is None:
        parsed_due = parsed_due.replace(tzinfo=timezone.utc)

    task = Task(
        user_id=user_id,
        title=title,
        course=course or None,
        due_at=parsed_due,
        estimated_duration_min=estimated_duration_min,
        importance=importance,
        type=type,
        status=TaskStatus.pending,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return RedirectResponse("/dashboard", status_code=303)