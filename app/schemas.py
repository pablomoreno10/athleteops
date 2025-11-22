from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from .enums import Importance, TaskStatus, TaskType, TransactionCategory


#Core task shape
class TaskBase(BaseModel):
    title: str
    course: str | None = None
    due_at: datetime
    estimated_duration_min: int = Field(gt=0)
    importance: Importance
    type: TaskType

#What the client sends when creating a task
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


#What the client sends when updating health attributes
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

class TransactionBase(BaseModel):
    date: date
    amount_cents: int
    merchant: str 
    category: TransactionCategory
    is_recurring: bool = False
    raw_description: str | None = None

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: int
    user_id: int
    time_created: datetime
    time_deleted: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class BudgetBase(BaseModel):
    category: TransactionCategory
    weekly_cents: int

class BudgetRead(BudgetBase):
    id: int
    user_id: int
    time_created: datetime

    model_config = ConfigDict(from_attributes=True)
