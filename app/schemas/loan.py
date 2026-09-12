import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.domain.loan import LoanStatus, LOAN_PERIOD_DAYS, MAX_LOAN_PERIOD_DAYS


class LoanCreate(BaseModel):
    book_id: uuid.UUID
    quantity: int = Field(default=1, ge=1)
    # Optional - falls back to LOAN_PERIOD_DAYS, capped at MAX_LOAN_PERIOD_DAYS.
    duration_days: Optional[int] = Field(
        default=LOAN_PERIOD_DAYS, ge=1, le=MAX_LOAN_PERIOD_DAYS
    )


class LoanOut(BaseModel):
    id: uuid.UUID
    book_id: uuid.UUID
    member_id: uuid.UUID
    loan_date: datetime
    due_date: datetime
    return_date: Optional[datetime]
    status: LoanStatus

    class Config:
        from_attributes = True
