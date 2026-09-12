from app.domain.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token


class InvalidCredentialsError(Exception):
    pass


class EmailAlreadyRegisteredError(Exception):
    pass


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, data: UserCreate, role: UserRole = UserRole.MEMBER) -> User:
        if self.user_repository.get_by_email(data.email):
            raise EmailAlreadyRegisteredError(f"Email {data.email} is already registered")

        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            role=role,
        )
        return self.user_repository.create(user)

    def authenticate(self, email: str, password: str) -> str:
        user = self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password")

        token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
        return token
