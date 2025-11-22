from enum import Enum

class TaskType(str, Enum):
    hw = "hw"
    exam = "exam"
    project = "project"
    other = "other"

class Importance(str, Enum):
    low = "low"
    med = "med"
    high = "high"

class TaskStatus(str, Enum):
    pending = "pending"
    scheduled = "scheduled"
    done = "done"

class TransactionCategory(str, Enum):
    dining = "dining"
    transportation = "transportation"
    groceries = "groceries"
    shopping = "shopping"
    school = "school"
    entertainment = "entertainment"
    health = "health"
    other = "other"


