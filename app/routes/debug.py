from fastapi import APIRouter
from workers.jobs import enqueue_weekly_for_all_users

router = APIRouter(prefix="/debug", tags=["debug"])

@router.post("/enqueue-weekly-all")
def enqueue_weekly_all():
    count = enqueue_weekly_for_all_users()
    return {"enqueued": count}
