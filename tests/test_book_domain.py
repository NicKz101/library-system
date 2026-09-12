import pytest

from app.domain.book import Book, BookNotAvailableError


def make_book(total=2, available=2):
    return Book(title="Clean Code", author="R. Martin", isbn="123", total_copies=total, available_copies=available)


def test_borrow_copy_decrements_available():
    book = make_book(total=2, available=2)
    book.borrow_copy()
    assert book.available_copies == 1


def test_borrow_copy_raises_when_none_available():
    book = make_book(total=1, available=0)
    with pytest.raises(BookNotAvailableError):
        book.borrow_copy()


def test_return_copy_increments_available():
    book = make_book(total=2, available=1)
    book.return_copy()
    assert book.available_copies == 2


def test_return_copy_never_exceeds_total():
    book = make_book(total=2, available=2)
    book.return_copy()
    assert book.available_copies == 2
