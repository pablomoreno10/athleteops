from fastapi import APIRouter, Depends, Query
from app.models import Budget
from sqlalchemy.orm import Session
from app.schemas import  BudgetRead, BudgetUpdate
from app.db import get_db
from app.auth import get_current_user_id

router = APIRouter(prefix="/finance",  tags=["finance"])


@router.get('/budgets', response_model=list[BudgetRead])
def get_budgets(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    budgets = db.query(Budget).filter_by(user_id=user_id).all()
    return budgets

#route to update budgets, if budget already present then we just update the weekly_cents
@router.post('/budgets', response_model=list[BudgetRead]) #BudgetRead because that describes what the API sends back
def set_budgets(budgets_in: list[BudgetUpdate], db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    updated_budget: list[Budget] = []

    for item in budgets_in:
        budget = (
            db.query(Budget)
            .filter_by(user_id=user_id, category=item.category)
            .one_or_none()
        )

        if budget:
            budget.weekly_cents = item.weekly_cents
        else:
            budget = Budget(
                user_id=user_id,
                category=item.category,
                weekly_cents=item.weekly_cents,
            )
            db.add(budget)

        updated_budget.append(budget)

    db.commit()
    for b in updated_budget:
        db.refresh(b)

    return updated_budget   

