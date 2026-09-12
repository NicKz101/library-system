import uuid
from typing import Optional
from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    category: Optional[str] = None
    total_copies: int = Field(default=1, ge=1)


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    total_copies: Optional[int] = Field(default=None, ge=1)


class BookOut(BaseModel):
    id: uuid.UUID
    title: str
    author: str
    isbn: str
    category: Optional[str]
    total_copies: int
    available_copies: int

    class Config:
        from_attributes = True
