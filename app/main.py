from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine, SessionLocal
from app.core.seed import seed_admin_user
from app.api.routers import auth_router, book_router, loan_router, user_router

# Import all domain models so SQLAlchemy registers them on Base.metadata
from app.domain import user, book, loan  # noqa: F401

Base.metadata.create_all(bind=engine)

# Make sure an admin account exists so nobody has to create one by hand.
with SessionLocal() as db:
    seed_admin_user(db)

app = FastAPI(
    title="Library Management System API",
    description="A simple library system demonstrating DDD, layered "
    "architecture (Repository/Service/Controller), and JWT auth.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(book_router.router)
app.include_router(loan_router.router)
app.include_router(user_router.router)


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "service": "library-management-api"}
