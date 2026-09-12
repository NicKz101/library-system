from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_admin
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserOut

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/", response_model=list[UserOut])
def list_users(
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    """Admin-only: list all registered users, used to identify who borrowed what."""
    return UserRepository(db).list_all()
