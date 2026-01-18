from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone, date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import HealthLog, Transactions, Task, Summary


@dataclass
class WeeklySummary:
    user_id: int
    start_ts: datetime
    end_ts: datetime
    avg_sleep_hours: float | None
    total_spend_cents: int
    danger_task_count: int


def get_week_window_utc(now: datetime | None = None) -> tuple[datetime, datetime]:
    """
      period_start = Monday 00:00 UTC
      period_end   = next Monday 00:00 UTC
    """
    if now is None:
        now = datetime.now(timezone.utc)

    # Snap to Monday 00:00 UTC
    monday_date = now.date() - timedelta(days=now.weekday())  # weekday(): Mon=0 ... Sun=6
    start_ts = datetime(monday_date.year, monday_date.month, monday_date.day, tzinfo=timezone.utc)
    end_ts = start_ts + timedelta(days=7)
    return start_ts, end_ts


def compute_weekly_summary(db: Session, user_id: int) -> WeeklySummary:
    start_ts, end_ts = get_week_window_utc()

    start_date = start_ts.date()
    end_date = end_ts.date() 

    avg_sleep_hours = (
        db.query(func.coalesce(func.avg(HealthLog.sleep_hours), 0))
        .filter(HealthLog.user_id == user_id)
        .filter(HealthLog.date >= start_date)
        .filter(HealthLog.date < end_date) 
        .scalar()
    )
    avg_sleep_hours = float(avg_sleep_hours or 0)

    total_spend = (
        db.query(func.coalesce(func.sum(Transactions.amount_cents), 0))
        .filter(Transactions.user_id == user_id)
        .filter(Transactions.time_created >= start_ts)
        .filter(Transactions.time_created < end_ts)
        .scalar()
    )
    total_spend_cents = int(total_spend or 0)

    danger_task_count = (
        db.query(func.count(Task.id))
        .filter(Task.user_id == user_id)
        .filter(Task.danger_flag.is_(True))
        .filter(Task.is_archived.is_(False))
        .scalar()
    )
    danger_task_count = int(danger_task_count or 0)

    return WeeklySummary(
        user_id=user_id,
        start_ts=start_ts,
        end_ts=end_ts,
        avg_sleep_hours=avg_sleep_hours,
        total_spend_cents=total_spend_cents,
        danger_task_count=danger_task_count,
    )


def save_weekly_summary(db: Session, weekly_summary: WeeklySummary) -> Summary:
    
    existing = (
        db.query(Summary)
        .filter(Summary.user_id == weekly_summary.user_id)
        .filter(Summary.period_start == weekly_summary.start_ts)
        .filter(Summary.period_end == weekly_summary.end_ts)
        .first()
    )

    if existing:
        existing.average_sleep = weekly_summary.avg_sleep_hours
        existing.danger_tasks = weekly_summary.danger_task_count
        existing.total_spend = weekly_summary.total_spend_cents 
        db.commit()
        db.refresh(existing)
        return existing

    new_summary = Summary(
        user_id=weekly_summary.user_id,
        period_start=weekly_summary.start_ts,
        period_end=weekly_summary.end_ts,
        average_sleep=weekly_summary.avg_sleep_hours,
        danger_tasks=weekly_summary.danger_task_count,
        total_spend=weekly_summary.total_spend_cents,  
    )
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    return new_summary
