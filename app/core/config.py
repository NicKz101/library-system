from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://library_user:library_pass@localhost:5432/library_db"
    SECRET_KEY: str = "change-this-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Used to auto-create the first admin account on startup (see core/seed.py),
    # so nobody has to run a manual SQL UPDATE just to get an ADMIN user.
    ADMIN_EMAIL: str = "admin@library.com"
    ADMIN_PASSWORD: str = "ChangeMe123!"
    ADMIN_FULL_NAME: str = "System Administrator"

    class Config:
        env_file = ".env"


settings = Settings()
