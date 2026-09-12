import uuid
from typing import Optional

from app.domain.book import Book
from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate, BookUpdate


class BookNotFoundError(Exception):
    pass


class DuplicateIsbnError(Exception):
    pass


class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def create_book(self, data: BookCreate) -> Book:
        if self.book_repository.get_by_isbn(data.isbn):
            raise DuplicateIsbnError(f"ISBN {data.isbn} already exists")

        book = Book(
            title=data.title,
            author=data.author,
            isbn=data.isbn,
            category=data.category,
            total_copies=data.total_copies,
            available_copies=data.total_copies,
        )
        return self.book_repository.create(book)

    def get_book(self, book_id: uuid.UUID) -> Book:
        book = self.book_repository.get_by_id(book_id)
        if not book:
            raise BookNotFoundError(f"Book {book_id} not found")
        return book

    def list_books(self, category: Optional[str] = None) -> list[Book]:
        return self.book_repository.list_all(category)

    def update_book(self, book_id: uuid.UUID, data: BookUpdate) -> Book:
        book = self.get_book(book_id)
        update_data = data.model_dump(exclude_unset=True)

        if "total_copies" in update_data:
            diff = update_data["total_copies"] - book.total_copies
            book.available_copies = max(0, book.available_copies + diff)

        for field, value in update_data.items():
            setattr(book, field, value)

        return self.book_repository.update(book)

    def delete_book(self, book_id: uuid.UUID) -> None:
        book = self.get_book(book_id)
        self.book_repository.delete(book)
