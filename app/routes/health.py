from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import HealthLog
from app.schemas import HealthLogRead, HealthLogUpdate

router = APIRouter(prefix="/health-log", tags=["health"])

# Temporary default until auth/user management exists
DEFAULT_USER_ID = 1


@router.post("/today", response_model=HealthLogRead)
def upsert_today_health_log(payload: HealthLogUpdate, db: Session = Depends(get_db)):
    today = date.today()
    data = payload.model_dump(exclude_unset=True)

    log = db.query(HealthLog).filter_by(user_id=DEFAULT_USER_ID, date=today).one_or_none()
    if log:
        for field, value in data.items():
            setattr(log, field, value)
    else:
        log = HealthLog(user_id=DEFAULT_USER_ID, date=today, **data)
        db.add(log)

    db.commit()
    db.refresh(log)
    return log


@router.get("/today", response_model=HealthLogRead | None)
def get_today_health_log(db: Session = Depends(get_db)):
    today = date.today()
    log = db.query(HealthLog).filter_by(user_id=DEFAULT_USER_ID, date=today).one_or_none()
    return log
