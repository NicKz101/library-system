from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password
from app.domain.user import User, UserRole
from app.repositories.user_repository import UserRepository


def seed_admin_user(db: Session) -> None:
    """
    Make sure at least one ADMIN account exists, so a fresh setup doesn't
    need a manual SQL UPDATE. Reads credentials from ADMIN_EMAIL /
    ADMIN_PASSWORD / ADMIN_FULL_NAME (see .env.example) and only creates
    the user if that email isn't already registered - safe to call on
    every startup.
    """
    repo = UserRepository(db)
    if repo.get_by_email(settings.ADMIN_EMAIL):
        return

    admin = User(
        email=settings.ADMIN_EMAIL,
        hashed_password=hash_password(settings.ADMIN_PASSWORD),
        full_name=settings.ADMIN_FULL_NAME,
        role=UserRole.ADMIN,
    )
    repo.create(admin)
    print(f"[seed] Created admin user: {settings.ADMIN_EMAIL}")
