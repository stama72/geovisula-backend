# geovisula-backend

FastAPI + SQLAlchemy backend for Geovisula.

## Database schema management

This backend now uses Alembic for schema versioning.

- `alembic/versions/0001_initial_schema.py` contains the initial schema.
- `migrate.py` runs `alembic upgrade head` using `DATABASE_URL`.
- `alembic/env.py` imports `models.py`, so the ORM metadata stays the source of truth for future revisions.

## Local setup

1. Install dependencies.
   - `pip install -r requirements.txt`
2. Set `DATABASE_URL` in your environment.
3. Apply migrations.
   - `python migrate.py`
4. Start the API.
   - `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`

## Production startup

The Render start command runs migrations before starting Uvicorn, so schema changes are applied automatically during deployment.

## Creating future migrations

When you change the ORM models in `models.py`, create a new Alembic revision and keep the migration history incremental.
