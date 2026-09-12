import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_admin
from app.domain.book import BookNotAvailableError
from app.domain.user import User
from app.repositories.book_repository import BookRepository
from app.repositories.loan_repository import LoanRepository
from app.schemas.loan import LoanCreate, LoanOut
from app.services.loan_service import (
    LoanService,
    LoanNotFoundError,
    LoanAlreadyReturnedError,
)

router = APIRouter(prefix="/api/loans", tags=["loans"])


def get_loan_service(db: Session = Depends(get_db)) -> LoanService:
    return LoanService(LoanRepository(db), BookRepository(db))


@router.post("/", response_model=list[LoanOut], status_code=status.HTTP_201_CREATED)
def borrow_book(
    data: LoanCreate,
    service: LoanService = Depends(get_loan_service),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.borrow_book(current_user.id, data.book_id, data.quantity, data.duration_days)
    except BookNotAvailableError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{loan_id}/return", response_model=LoanOut)
def return_book(
    loan_id: uuid.UUID,
    service: LoanService = Depends(get_loan_service),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.return_book(loan_id)
    except LoanNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except LoanAlreadyReturnedError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/me", response_model=list[LoanOut])
def my_loans(
    service: LoanService = Depends(get_loan_service),
    current_user: User = Depends(get_current_user),
):
    return service.list_member_loans(current_user.id)


@router.get("/", response_model=list[LoanOut])
def all_loans(
    service: LoanService = Depends(get_loan_service),
    _admin: User = Depends(require_admin),
):
    """Admin-only: view every loan in the system."""
    return service.list_all_loans()
