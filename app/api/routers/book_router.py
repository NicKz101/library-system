import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_admin
from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate, BookOut, BookUpdate
from app.services.book_service import BookService, BookNotFoundError, DuplicateIsbnError

router = APIRouter(prefix="/api/books", tags=["books"])


def get_book_service(db: Session = Depends(get_db)) -> BookService:
    return BookService(BookRepository(db))


@router.get("/", response_model=list[BookOut])
def list_books(category: Optional[str] = None, service: BookService = Depends(get_book_service)):
    """Public endpoint: any authenticated member can browse the catalog."""
    return service.list_books(category)


@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: uuid.UUID, service: BookService = Depends(get_book_service)):
    try:
        return service.get_book(book_id)
    except BookNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(
    data: BookCreate,
    service: BookService = Depends(get_book_service),
    _admin=Depends(require_admin),
):
    try:
        return service.create_book(data)
    except DuplicateIsbnError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{book_id}", response_model=BookOut)
def update_book(
    book_id: uuid.UUID,
    data: BookUpdate,
    service: BookService = Depends(get_book_service),
    _admin=Depends(require_admin),
):
    try:
        return service.update_book(book_id, data)
    except BookNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: uuid.UUID,
    service: BookService = Depends(get_book_service),
    _admin=Depends(require_admin),
):
    try:
        service.delete_book(book_id)
    except BookNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
