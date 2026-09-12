import uuid
from typing import Optional

from app.domain.book import BookNotAvailableError
from app.domain.loan import Loan, LOAN_PERIOD_DAYS
from app.repositories.book_repository import BookRepository
from app.repositories.loan_repository import LoanRepository


class LoanNotFoundError(Exception):
    pass


class LoanAlreadyReturnedError(Exception):
    pass


class LoanService:
    """
    Orchestrates borrowing/returning. The actual availability invariant
    lives on the Book aggregate (borrow_copy/return_copy); this service
    just coordinates the Book and Loan repositories within one operation.
    """

    def __init__(self, loan_repository: LoanRepository, book_repository: BookRepository):
        self.loan_repository = loan_repository
        self.book_repository = book_repository

    def borrow_book(
        self,
        member_id: uuid.UUID,
        book_id: uuid.UUID,
        quantity: int = 1,
        duration_days: Optional[int] = None,
    ) -> list[Loan]:
        book = self.book_repository.get_by_id(book_id)
        if not book:
            raise ValueError(f"Book {book_id} not found")

        # Check upfront so a request for more copies than exist fails
        # cleanly, instead of partially borrowing what's left.
        if book.available_copies < quantity:
            raise BookNotAvailableError(
                f"Only {book.available_copies} cop{'y' if book.available_copies == 1 else 'ies'} "
                f"of '{book.title}' available"
            )

        due_date = Loan.default_due_date(duration_days or LOAN_PERIOD_DAYS)

        for _ in range(quantity):
            book.borrow_copy()
        self.book_repository.update(book)

        return [
            self.loan_repository.create(
                Loan(book_id=book_id, member_id=member_id, due_date=due_date)
            )
            for _ in range(quantity)
        ]

    def return_book(self, loan_id: uuid.UUID) -> Loan:
        loan = self.loan_repository.get_by_id(loan_id)
        if not loan:
            raise LoanNotFoundError(f"Loan {loan_id} not found")
        if loan.return_date is not None:
            raise LoanAlreadyReturnedError(f"Loan {loan_id} was already returned")

        loan.mark_returned()
        self.loan_repository.update(loan)

        book = self.book_repository.get_by_id(loan.book_id)
        book.return_copy()
        self.book_repository.update(book)

        return loan

    def list_member_loans(self, member_id: uuid.UUID) -> list[Loan]:
        loans = self.loan_repository.list_by_member(member_id)
        for loan in loans:
            loan.refresh_status()
        return loans

    def list_all_loans(self) -> list[Loan]:
        loans = self.loan_repository.list_all()
        for loan in loans:
            loan.refresh_status()
        return loans
