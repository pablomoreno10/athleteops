from app.db import SessionLocal
from app.models import User
from app.services.weekly_summary import compute_weekly_summary, save_weekly_summary

def run_weekly_summary_job(user_id: int) -> int:
    db = SessionLocal()
    try:
        summary = compute_weekly_summary(db, user_id=user_id)
        saved = save_weekly_summary(db, summary)
        return saved.id
    finally:
        db.close()

def enqueue_weekly_for_all_users() -> int:
    from app.queues import default_queue

    db = SessionLocal()
    try:
        user_ids = [u.id for u in db.query(User.id).all()]
    finally:
        db.close()

    for uid in user_ids:
        default_queue.enqueue(run_weekly_summary_job, uid)

    return len(user_ids)
