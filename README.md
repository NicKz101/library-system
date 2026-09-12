# Library Management System

This is my final project for the **Coding Factory (AUEB)** program: a small library
system for lending out books, built to practice clean architecture and full-stack
development rather than to reinvent library software.

It includes:
- **Domain-Driven Design** — the business rules live inside the domain entities themselves (`Book`, `Loan`, `User`), not scattered across services
- **Layered architecture**: Repository → Service → Controller (API Router)
- **REST API** built with FastAPI, self-documented via **Swagger** (`/docs`)
- **JWT authentication / role-based authorization** (ADMIN / MEMBER), enforced on both backend and frontend
- **React** frontend (fully in English, admin and member views alike) with Tailwind CSS and the Context API for state management
- **PostgreSQL**, running in **Docker**
- **Unit tests** for the domain layer with pytest

---

## Architecture

```
library-system/
├── app/
│   ├── domain/          # Entities + business rules (Book, Loan, User)
│   ├── repositories/    # DB access layer (SQLAlchemy queries)
│   ├── services/        # Business logic orchestration
│   ├── schemas/         # Pydantic DTOs (request/response validation)
│   ├── api/routers/     # FastAPI controllers (HTTP layer)
│   ├── core/            # config, DB session, security, auth deps, admin seed
│   └── main.py          # FastAPI app entrypoint
├── tests/               # pytest unit tests (domain logic)
├── frontend/            # React + Vite + Tailwind SPA
│   └── src/
│       ├── api/         # axios clients, one per resource
│       ├── context/     # AuthContext (JWT, role)
│       ├── components/  # Navbar, BookCard, LoanTable, OverdueLoansModal, ProtectedRoute
│       └── pages/       # Login, Register, Books, MyLoans, AdminLoans
├── docker-compose.yml   # Postgres + FastAPI API
├── Dockerfile           # backend image
└── requirements.txt
```


---

## Prerequisites

- [Docker](https://www.docker.com/) & Docker Compose
- [Node.js](https://nodejs.org/) 18+ (for the frontend)
- (Optional) Python 3.12+ if you'd rather run the backend locally without Docker

---

## Build & run — step by step

### 1. Clone the repository

```bash
git clone <your-github-repo-url>
cd library-system
```

### 2. Backend + database (via Docker)

`docker-compose.yml` brings up PostgreSQL **and** the FastAPI backend together.

```bash
docker compose up --build
```

This will:
- Build the backend image (`Dockerfile`)
- Start a PostgreSQL container (`library_db`)
- Wait for the database to be healthy, then start the API
- Automatically create the tables (via SQLAlchemy's `Base.metadata.create_all`)

The backend will be available at: **http://localhost:8000**
Swagger docs: **http://localhost:8000/docs**

To stop it:
```bash
docker compose down
```

To also wipe the database data:
```bash
docker compose down -v
```

#### Alternative: running the backend without Docker

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# You still need a PostgreSQL instance somewhere — this spins up just the DB container:
docker compose up db -d

cp .env.example .env   # adjust DATABASE_URL if needed

uvicorn app.main:app --reload
```

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env   # adjust VITE_API_URL if the backend runs elsewhere
npm run dev
```

The frontend will be available at: **http://localhost:5173**

#### Production build

```bash
npm run build
```

The output (static files) lands in `frontend/dist/` and can be served by any static file
server (e.g. Nginx, Vercel, Netlify).

---

## Using the app

1. Open **http://localhost:5173**
2. **Sign up** (this always creates a `MEMBER` account)
3. Browse the **book catalog** and borrow a book — you can pick a return deadline of up to
   20 days before confirming
4. Check your loans under **"My Loans"**; if anything is overdue, you'll see it flagged
   there too, and you'll get a warning pop-up the next time you log in

### Creating an admin user

Signing up through the UI always creates a `MEMBER` account. You don't need to touch the
database by hand though: on every startup, the backend checks whether the admin account
defined by `ADMIN_EMAIL` / `ADMIN_PASSWORD` / `ADMIN_FULL_NAME` (see `.env.example` /
`docker-compose.yml`) already exists, and creates it automatically if not (see
`app/core/seed.py`, wired up in `app/main.py`).

With the default `.env.example` values, that means an admin account is ready to use right
after `docker compose up --build`:

- **Email:** `admin@library.com`
- **Password:** `ChangeMe123!`

Change `ADMIN_EMAIL` / `ADMIN_PASSWORD` before deploying anywhere real — the seed script
only runs once per email (it does nothing if that email is already registered), so changing
the password afterwards means updating it through the database, same as any other user.

If you want a **second** admin, you can still promote any existing account by hand:

```bash
docker exec -it library_db psql -U library_user -d library_db \
  -c "UPDATE users SET role = 'ADMIN' WHERE email = 'your-email@example.com';"
```

As an admin you can add/edit/delete books, and see **every** loan in the system
(`/admin/loans`), including which ones are overdue.

---

## API documentation (Swagger)

Once the backend is running, the full REST API reference is available at:

**http://localhost:8000/docs** (Swagger UI)
**http://localhost:8000/redoc** (ReDoc, an alternative UI)

---

## Testing

```bash
# Inside the venv, or inside the backend container:
pytest
```

The tests cover the core domain logic:
- `Book.borrow_copy()` / `return_copy()` — availability invariants
- `Loan.mark_returned()` / `refresh_status()` — lifecycle transitions, including the
  overdue check and the 1–20 day loan duration validation

For integration testing of the REST API, you can point **Postman** (or any HTTP client) at
the OpenAPI schema exposed under `/docs`.

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, SQLAlchemy |
| Database | PostgreSQL (in Docker) |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Frontend | React, Vite, Tailwind CSS, React Router, Axios |
| Docs | Swagger / OpenAPI (auto-generated) |
| Testing | pytest |
| Containerization | Docker, Docker Compose |
