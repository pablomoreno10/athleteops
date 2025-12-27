from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone, date
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import HealthLog, Transactions, Task


@dataclass
class WeeklySummary:
    user_id: int
    start_ts: datetime
    end_ts: datetime
    avg_sleep_hours: float | None
    total_spend_cents: int
    danger_task_count: int


def compute_weekly_summary(db: Session, user_id: int, *, days: int = 7) -> WeeklySummary:

    end_ts = datetime.now(timezone.utc)
    start_ts = end_ts - timedelta(days=days)

    #1)Average sleep over last 7 days
    start_date = start_ts.date()
    end_date = end_ts.date()

    avg_sleep = (
        db.query(func.avg(HealthLog.sleep_hours))
        .filter(HealthLog.user_id == user_id)
        .filter(HealthLog.date >= start_date)
        .filter(HealthLog.date <= end_date)
        .scalar()
    )
    avg_sleep_hours = float(avg_sleep) if avg_sleep is not None else 0

    #2) Total spend over last 7 days (sum of amount_cents)
    total_spend = (
        db.query(func.coalesce(func.sum(Transactions.amount_cents), 0))
        .filter(Transactions.user_id == user_id)
        .filter(Transactions.time_created >= start_ts) 
        .filter(Transactions.time_created < end_ts)
        .scalar()
    )
    total_spend_cents = int(total_spend or 0)

    #3) Danger tasks count
    danger_task_count = (
        db.query(func.count(Task.id))
        .filter(Task.user_id == user_id)
        .filter(Task.danger_flag.is_(True))
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
