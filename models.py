from datetime import date
from pydantic import BaseModel

class Task(BaseModel):
    user_id: int
    title: str
    course: course
    type: type
    due_at: date
    estimated_duration_min: int
    importance: importance
    status: status
    scheduled_start: date
    scheduled_end: date
    danger_flag: bool
    is_archived: bool
    created_at: date
    updated_at: date

