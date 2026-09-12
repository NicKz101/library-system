import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.domain.loan import Loan, LoanStatus


class LoanRepository:
    """Encapsulates all direct DB access for the Loan entity."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, loan_id: uuid.UUID) -> Optional[Loan]:
        return self.db.query(Loan).filter(Loan.id == loan_id).first()

    def list_by_member(self, member_id: uuid.UUID) -> list[Loan]:
        return self.db.query(Loan).filter(Loan.member_id == member_id).all()

    def list_all(self) -> list[Loan]:
        return self.db.query(Loan).all()

    def list_active_for_book(self, book_id: uuid.UUID) -> list[Loan]:
        return (
            self.db.query(Loan)
            .filter(Loan.book_id == book_id, Loan.status == LoanStatus.ACTIVE)
            .all()
        )

    def create(self, loan: Loan) -> Loan:
        self.db.add(loan)
        self.db.commit()
        self.db.refresh(loan)
        return loan

    def update(self, loan: Loan) -> Loan:
        self.db.commit()
        self.db.refresh(loan)
        return loan
