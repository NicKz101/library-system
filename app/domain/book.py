import uuid

from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class BookNotAvailableError(Exception):
    """Raised when trying to borrow a book with zero available copies."""
    pass


class Book(Base):
    """
    Book is the aggregate root for the catalog. Availability rules live
    here rather than in the service layer, so the invariant
    'available_copies <= total_copies' can never be violated from outside.
    """
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    isbn = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=True)
    total_copies = Column(Integer, nullable=False, default=1)
    available_copies = Column(Integer, nullable=False, default=1)

    loans = relationship("Loan", back_populates="book", cascade="all, delete-orphan")

    def borrow_copy(self) -> None:
        """Domain rule: cannot borrow a book with no available copies."""
        if self.available_copies <= 0:
            raise BookNotAvailableError(f"No available copies of '{self.title}'")
        self.available_copies -= 1

    def return_copy(self) -> None:
        """Domain rule: available copies can never exceed total copies."""
        if self.available_copies < self.total_copies:
            self.available_copies += 1
