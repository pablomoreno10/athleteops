from fastapi import APIRouter, Depends, Form, Query, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta, timezone

from app.db import get_db

from app.models import Transactions
from app.schemas import TransactionCreate, TransactionRead, TransactionGraph
from app.enums import TransactionCategory
from app.auth import get_current_user_id

from sqlalchemy import func

router = APIRouter(prefix="/finance", tags=["finance"])


#manually add a transaction
@router.post('/transactions', response_model=TransactionRead)
def create_transaction(transaction_in: TransactionCreate, db: Session=Depends(get_db), user_id: int = Depends(get_current_user_id)):
        transaction_out = Transactions(
                user_id=user_id,
                **transaction_in.model_dump(),
                #model_dump used to serialize the pydantic model into a python dictionary
        )
        db.add(transaction_out)
        db.commit()
        db.refresh(transaction_out)
        return transaction_out

#get transactions from the last 7 days
@router.get("/transactions/week", response_model=list[TransactionRead])
def list_transactions(days_ago: int = Query(7, ge=1, description="Number of days to look back"), db: Session=Depends(get_db), user_id: int = Depends(get_current_user_id)):
    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=days_ago)
    weekly_summary = db.query(Transactions).filter(Transactions.user_id == user_id, Transactions.time_created >= start_date).all()
    return weekly_summary

@router.get("/transactions/week/summary", response_model=list[TransactionGraph])
def transactions_summary(
    days_ago: int = Query(14, ge=1), 
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=days_ago)
    
    summary = db.query(
        Transactions.category, 
        func.sum(Transactions.amount_cents).label("total_cents")
    ).filter(
        Transactions.time_created >= start_date,
        Transactions.user_id == user_id
    ).group_by(Transactions.category).all()
    
    return summary
    

@router.post("/transactions/form")
def create_transaction_from_form(
    merchant: str = Form(...),
    amount_cents: int = Form(...),
    category: str = Form(...),
    raw_description: str | None = Form(None),
    is_recurring: bool = Form(False),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    try:
        category_enum = TransactionCategory(category)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid category")

    transaction_out = Transactions(
        user_id=user_id,
        date=date.today(),
        amount_cents=amount_cents,
        merchant=merchant,
        category=category_enum,
        raw_description=raw_description if raw_description not in ("", None) else None,
        is_recurring=is_recurring,
    )
    db.add(transaction_out)
    db.commit()
    db.refresh(transaction_out)
    return RedirectResponse("/dashboard", status_code=303)


