import enum
import uuid
from datetime import datetime, timezone, timedelta

from sqlalchemy import Column, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base

# Default loan period if the member doesn't ask for a specific duration.
LOAN_PERIOD_DAYS = 14

# Members can request a longer loan, but never more than this.
MAX_LOAN_PERIOD_DAYS = 20


class LoanStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"


class Loan(Base):
    """
    Represents a single borrowing transaction linking a Member (User) to a Book.
    Encapsulates its own lifecycle: active -> returned, or active -> overdue.
    """
    __tablename__ = "loans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    member_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # timezone=True stores these as Postgres `timestamptz`. Without it,
    # values are saved as naive timestamps, the API serializes them with
    # no UTC offset, and the browser ends up parsing them as local time -
    # which is why loan dates used to show up a few hours off.
    loan_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    due_date = Column(DateTime(timezone=True), nullable=False)
    return_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(LoanStatus), nullable=False, default=LoanStatus.ACTIVE)

    book = relationship("Book", back_populates="loans")
    member = relationship("User", back_populates="loans")

    @staticmethod
    def default_due_date(days: int = LOAN_PERIOD_DAYS) -> datetime:
        """Due date `days` from now (UTC). Must be 1..MAX_LOAN_PERIOD_DAYS."""
        if not 1 <= days <= MAX_LOAN_PERIOD_DAYS:
            raise ValueError(
                f"Loan duration must be between 1 and {MAX_LOAN_PERIOD_DAYS} days"
            )
        return datetime.now(timezone.utc) + timedelta(days=days)

    def mark_returned(self) -> None:
        self.return_date = datetime.now(timezone.utc)
        self.status = LoanStatus.RETURNED

    def refresh_status(self) -> None:
        """Recompute status based on due_date, unless already returned."""
        if self.status == LoanStatus.RETURNED:
            return
        due = self.due_date
        # Older rows created before this column became timestamptz may
        # still be naive - treat them as UTC rather than crash.
        if due.tzinfo is None:
            due = due.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > due:
            self.status = LoanStatus.OVERDUE
        else:
            self.status = LoanStatus.ACTIVE
