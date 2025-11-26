from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.db import get_db

from app.models import Transactions
from app.schemas import TransactionCreate, TransactionRead

router = APIRouter(prefix="/finance", tags=["finance"])


DEFAULT_USER_ID = 1

#manually add a transaction
@router.post('/transactions', response_model=TransactionRead)
def create_transaction(transaction_in: TransactionCreate, db: Session=Depends(get_db)):
        transaction_out = Transactions(
                user_id=DEFAULT_USER_ID,
                **transaction_in.model_dump(),
                #model_dump used to serialize the pydantic model into a python dictionary
        )
        db.add(transaction_out)
        db.commit()
        db.refresh(transaction_out)
        return transaction_out

#get transactions from the last 7 days
@router.get("/transactions/week", response_model=list[TransactionRead])
def list_transactions(days_ago: int = Query(7, ge=1, description="Number of days to look back"), db: Session=Depends(get_db)):
    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=days_ago)
    weekly_transactions = db.query(Transactions).filter(Transactions.time_created >= start_date).all()
    return weekly_transactions
