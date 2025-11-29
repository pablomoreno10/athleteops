from datetime import date

from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
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


@router.post("/today/form")
def upsert_today_health_log_form(
    sleep_hours: float | None = Form(None),
    hydration_liters: float | None = Form(None),
    exercise_minutes: int | None = Form(None),
    prayer_minutes: int | None = Form(None),
    social_media_minutes: int | None = Form(None),
    notes: str | None = Form(None),
    db: Session = Depends(get_db),
):
    today = date.today()
    # Convert blank strings to None so optional fields behave
    data = {
        "sleep_hours": sleep_hours if sleep_hours not in ("", None) else None,
        "hydration_liters": hydration_liters if hydration_liters not in ("", None) else None,
        "exercise_minutes": exercise_minutes if exercise_minutes not in ("", None) else None,
        "prayer_minutes": prayer_minutes if prayer_minutes not in ("", None) else None,
        "social_media_minutes": social_media_minutes if social_media_minutes not in ("", None) else None,
        "notes": notes if notes not in ("", None) else None,
    }

    log = db.query(HealthLog).filter_by(user_id=DEFAULT_USER_ID, date=today).one_or_none()
    if log:
        for field, value in data.items():
            setattr(log, field, value)
    else:
        log = HealthLog(user_id=DEFAULT_USER_ID, date=today, **data)
        db.add(log)

    db.commit()
    db.refresh(log)
    return RedirectResponse("/", status_code=303)


@router.get("/today", response_model=HealthLogRead | None)
def get_today_health_log(db: Session = Depends(get_db)):
    today = date.today()
    log = db.query(HealthLog).filter_by(user_id=DEFAULT_USER_ID, date=today).one_or_none()
    return log
