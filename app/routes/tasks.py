from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.enums import TaskStatus
from app.models import Task
from app.schemas import TaskCreate, TaskRead

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Temporary default until auth/user management exists
DEFAULT_USER_ID = 1


@router.post("/", response_model=TaskRead)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    task = Task(
        user_id=DEFAULT_USER_ID,
        status=TaskStatus.pending,
        **task_in.model_dump(),
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/", response_model=list[TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).order_by(Task.due_at.asc()).all()
    return tasks
