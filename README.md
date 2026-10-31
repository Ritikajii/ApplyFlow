# ApplyFlow – Job Application Tracker

ApplyFlow is a backend application built with FastAPI that helps users manage and track their job applications and interview processes.

## Features

- User registration and login
- Password hashing and JWT-based authentication
- User-specific application management
- Track companies, job roles and application statuses
- Manage interview rounds
- Dashboard statistics for job applications
- PostgreSQL database integration
- Database migrations using Alembic
- API documentation with Swagger UI

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL (Neon)
- **ORM:** SQLAlchemy
- **Authentication:** JWT, pwdlib (Argon2)
- **Validation:** Pydantic
- **Database Migrations:** Alembic
- **Testing:** Pytest
- **Package Management:** uv

## Project Structure

```text
applyflow/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── config.py
│   ├── dependencies.py
│   ├── security.py
│   └── auth.py
├── migrations/
│   ├── versions/
│   │   └── e976bb86ebc0_initial_schema.py
│   └── env.py
├── tests/
│   ├── conftest.py
│   └── test_auth.py
├── src/
│   └── applyflow/
│       └── __init__.py
├── alembic.ini
├── pyproject.toml
├── uv.lock
├── .gitignore
├── .env.example
└── README.md```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd applyflow
```

### 2. Install dependencies

Install uv, then run:

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=your_postgresql_connection_string
JWT_SECRET_KEY=your_secret_key
```

Use your own database URL and a securely generated JWT secret.

### 4. Run database migrations

```bash
uv run alembic upgrade head
```

### 5. Start the development server

```bash
uv run uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, access:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Database

ApplyFlow uses PostgreSQL for persistent data storage and SQLAlchemy for database operations. Alembic manages database schema migrations.

## Security

- Passwords are stored as secure hashes.
- JWT tokens are used for authentication.
- Environment variables are used for sensitive configuration.
- User-specific resources are protected through authentication.

## Future Improvements

- Email notifications for upcoming interviews
- Application analytics and visualizations
- Automated interview reminders

---

**ApplyFlow** – Organize your job search, track your progress, and stay prepared.