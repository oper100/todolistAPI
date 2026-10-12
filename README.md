# Todo List API

REST API for personal todo lists, built with FastAPI, SQLModel and PostgreSQL.
Users register, log in with a JWT token and manage only their own todos.

## Features

- Registration and login (JWT bearer tokens, passwords hashed with Argon2)
- CRUD for todos: create, list (with `skip` / `limit`), get, replace (`PUT`), update (`PATCH`), delete
- Each user sees only their own todos
- Database migrations with Alembic
- Docker and docker-compose setup
- Tests with pytest

## Run with Docker

You need Docker with Docker Compose.

```bash
git clone <repo-url>
cd todolistAPI_project

cp .env.example .env       # Windows: copy .env.example .env
# edit .env: set SECRET_KEY and POSTGRES_PASSWORD

docker compose up --build
```

Swagger docs: http://localhost:8000/docs

The API container applies the database migrations on every start, then runs the server.
Data is stored in a Docker volume, so it survives `docker compose down`.
Use `docker compose down -v` to delete the data too.

Look into the database:

```bash
docker compose exec postgres psql -U todo_user -d todolist
```

## Run without Docker

You need Python 3.10+ and a running PostgreSQL.

```bash
python -m venv venv
venv\Scripts\activate      # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env       # Windows: copy .env.example .env
# edit .env: set SECRET_KEY and DATABASE_URL

alembic upgrade head       # create the tables
uvicorn app.main:app --reload
```

Quick PostgreSQL for this mode:

```bash
docker run -d --name todo-postgres -e POSTGRES_USER=todo_user -e POSTGRES_PASSWORD=change-me -e POSTGRES_DB=todolist -p 5432:5432 -v todo_pgdata:/var/lib/postgresql/data postgres:17
```

## Settings (.env)

| Variable | Used by | Description |
|---|---|---|
| `SECRET_KEY` | both modes | Key for signing JWT tokens (required) |
| `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` | Docker | Database user, password and name |
| `DATABASE_URL` | without Docker | Database URL, e.g. `postgresql+psycopg://user:password@localhost:5432/todolist` |

## API

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/register` | no | Create a user |
| `POST` | `/auth/token` | no | Log in, get a token |
| `GET` | `/todos/` | yes | List your todos |
| `POST` | `/todos/` | yes | Create a todo |
| `GET` | `/todos/{id}` | yes | Get a todo |
| `PUT` | `/todos/{id}` | yes | Replace a todo |
| `PATCH` | `/todos/{id}` | yes | Partially update a todo |
| `DELETE` | `/todos/{id}` | yes | Delete a todo |

## Migrations

After changing a model in `app/models.py`:

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

Always read the generated file in `alembic/versions/` before applying it.

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

Tests use an in-memory SQLite database and do not touch PostgreSQL.
