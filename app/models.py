from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Enum as SAEnum, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .enums import Importance, TaskStatus, TaskType, TransactionCategory

class Base(DeclarativeBase):
    #Shared declarative base for all models.
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    course: Mapped[str | None] = mapped_column(String(100))
    type: Mapped[TaskType] = mapped_column(SAEnum(TaskType, name="task_type_enum"), nullable=False)
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    estimated_duration_min: Mapped[int] = mapped_column(Integer, nullable=False)
    importance: Mapped[Importance] = mapped_column(SAEnum(Importance, name="task_importance_enum"), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(SAEnum(TaskStatus, name="task_status_enum"),nullable=False,server_default=TaskStatus.pending.value, )
    scheduled_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    scheduled_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    danger_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
    time_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    time_updated: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class HealthLog(Base):
    __tablename__ = "health_logs"
    __table_args__ = (UniqueConstraint("user_id", "date", name="uq_health_logs_user_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    sleep_hours: Mapped[float | None] = mapped_column(Float)
    hydration_liters: Mapped[float | None] = mapped_column(Float)
    exercise_minutes: Mapped[int | None] = mapped_column(Integer)
    prayer_minutes: Mapped[int | None] = mapped_column(Integer)
    social_media_minutes: Mapped[int | None] = mapped_column(Integer)
    notes: Mapped[str | None] = mapped_column(Text)
    time_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    time_updated: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class Transactions(Base):
    __tablename__ = "transaction_logs"
    

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    merchant: Mapped[str] = mapped_column(String(50), nullable=False)
    raw_description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[TransactionCategory] = mapped_column(SAEnum(TransactionCategory,name='transaction_category_enum'), nullable=False)
    is_recurring: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
    time_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    time_deleted: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class Budget(Base):
    __tablename__ = "budgets"
    
    __table_args__ = (UniqueConstraint("user_id", "category", name="uq_budget_user_category"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    category: Mapped[TransactionCategory] = mapped_column(SAEnum(TransactionCategory,name='transaction_category_enum'), nullable=False)
    weekly_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    time_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


