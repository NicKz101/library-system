import uuid
from datetime import datetime, timedelta, timezone

import pytest

from app.domain.book import Book, BookNotAvailableError
from app.domain.loan import Loan, LoanStatus, LOAN_PERIOD_DAYS, MAX_LOAN_PERIOD_DAYS
from app.services.loan_service import (
    LoanService,
    LoanNotFoundError,
    LoanAlreadyReturnedError,
)


class FakeBookRepository:
    """In-memory stand-in - just enough of the real repo's interface for these tests."""

    def __init__(self, books=None):
        self._books = {b.id: b for b in (books or [])}

    def get_by_id(self, book_id):
        return self._books.get(book_id)

    def update(self, book):
        self._books[book.id] = book
        return book


class FakeLoanRepository:
    def __init__(self):
        self._loans = {}

    def get_by_id(self, loan_id):
        return self._loans.get(loan_id)

    def create(self, loan):
        if loan.id is None:
            loan.id = uuid.uuid4()
        self._loans[loan.id] = loan
        return loan

    def update(self, loan):
        self._loans[loan.id] = loan
        return loan


def make_book(total=3, available=3):
    return Book(
        id=uuid.uuid4(),
        title="Clean Code",
        author="R. Martin",
        isbn="123",
        total_copies=total,
        available_copies=available,
    )


def make_service(book):
    book_repo = FakeBookRepository([book])
    loan_repo = FakeLoanRepository()
    return LoanService(loan_repo, book_repo), book_repo, loan_repo


def test_borrow_single_copy_decrements_availability():
    book = make_book(total=2, available=2)
    service, book_repo, _ = make_service(book)

    loans = service.borrow_book(uuid.uuid4(), book.id, quantity=1)

    assert len(loans) == 1
    assert book_repo.get_by_id(book.id).available_copies == 1


def test_borrow_multiple_copies_creates_one_loan_per_copy():
    book = make_book(total=5, available=5)
    service, book_repo, _ = make_service(book)

    loans = service.borrow_book(uuid.uuid4(), book.id, quantity=3)

    assert len(loans) == 3
    assert len({loan.id for loan in loans}) == 3  # each loan is distinct
    assert book_repo.get_by_id(book.id).available_copies == 2


def test_borrow_more_than_available_raises_and_changes_nothing():
    book = make_book(total=2, available=2)
    service, book_repo, loan_repo = make_service(book)

    with pytest.raises(BookNotAvailableError):
        service.borrow_book(uuid.uuid4(), book.id, quantity=3)

    # Nothing should have been touched - it's all-or-nothing.
    assert book_repo.get_by_id(book.id).available_copies == 2
    assert loan_repo._loans == {}


def test_borrow_unknown_book_raises_value_error():
    book = make_book()
    service, _, _ = make_service(book)

    with pytest.raises(ValueError):
        service.borrow_book(uuid.uuid4(), uuid.uuid4(), quantity=1)


def test_borrow_without_duration_uses_default_period():
    book = make_book()
    service, _, _ = make_service(book)

    [loan] = service.borrow_book(uuid.uuid4(), book.id, quantity=1)

    expected = datetime.now(timezone.utc) + timedelta(days=LOAN_PERIOD_DAYS)
    assert abs((loan.due_date - expected).total_seconds()) < 5


def test_borrow_with_requested_duration_is_respected():
    book = make_book()
    service, _, _ = make_service(book)

    [loan] = service.borrow_book(uuid.uuid4(), book.id, quantity=1, duration_days=MAX_LOAN_PERIOD_DAYS)

    expected = datetime.now(timezone.utc) + timedelta(days=MAX_LOAN_PERIOD_DAYS)
    assert abs((loan.due_date - expected).total_seconds()) < 5


def test_return_book_marks_returned_and_restores_availability():
    book = make_book(total=2, available=1)  # one copy already out
    service, book_repo, loan_repo = make_service(book)
    loan = loan_repo.create(Loan(id=uuid.uuid4(), book_id=book.id, due_date=Loan.default_due_date()))

    returned = service.return_book(loan.id)

    assert returned.status == LoanStatus.RETURNED
    assert returned.return_date is not None
    assert book_repo.get_by_id(book.id).available_copies == 2


def test_return_unknown_loan_raises_not_found():
    book = make_book()
    service, _, _ = make_service(book)

    with pytest.raises(LoanNotFoundError):
        service.return_book(uuid.uuid4())


def test_return_already_returned_loan_raises():
    book = make_book(total=2, available=2)
    service, _, loan_repo = make_service(book)
    loan = loan_repo.create(Loan(id=uuid.uuid4(), book_id=book.id, due_date=Loan.default_due_date()))
    service.return_book(loan.id)

    with pytest.raises(LoanAlreadyReturnedError):
        service.return_book(loan.id)