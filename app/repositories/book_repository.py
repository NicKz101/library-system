import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.domain.book import Book


class BookRepository:
    """Encapsulates all direct DB access for the Book entity."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, book_id: uuid.UUID) -> Optional[Book]:
        return self.db.query(Book).filter(Book.id == book_id).first()

    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        return self.db.query(Book).filter(Book.isbn == isbn).first()

    def list_all(self, category: Optional[str] = None) -> list[Book]:
        query = self.db.query(Book)
        if category:
            query = query.filter(Book.category == category)
        return query.all()

    def create(self, book: Book) -> Book:
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def update(self, book: Book) -> Book:
        self.db.commit()
        self.db.refresh(book)
        return book

    def delete(self, book: Book) -> None:
        self.db.delete(book)
        self.db.commit()
