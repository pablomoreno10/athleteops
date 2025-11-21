from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from .enums import Importance, TaskStatus, TaskType


class TaskBase(BaseModel):
    title: str
    course: str | None = None
    due_at: datetime
    estimated_duration_min: int = Field(gt=0)
    importance: Importance
    type: TaskType


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    user_id: int
    status: TaskStatus
    scheduled_start: datetime | None = None
    scheduled_end: datetime | None = None
    danger_flag: bool = False
    is_archived: bool = False
    time_created: datetime
    time_updated: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class HealthLogUpdate(BaseModel):
    sleep_hours: float | None = None
    hydration_liters: float | None = None
    exercise_minutes: int | None = None
    prayer_minutes: int | None = None
    social_media_minutes: int | None = None
    notes: str | None = None


class HealthLogRead(HealthLogUpdate):
    id: int
    user_id: int
    date: date
    time_created: datetime
    time_updated: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
