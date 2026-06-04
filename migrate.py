from __future__ import annotations

import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect


load_dotenv()


def run_migrations() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL is required")

    alembic_ini = Path(__file__).resolve().parent / "alembic.ini"
    if not alembic_ini.exists():
        raise SystemExit(f"Alembic configuration not found: {alembic_ini}")

    config = Config(str(alembic_ini))
    config.set_main_option("sqlalchemy.url", database_url)

    engine = create_engine(database_url)
    with engine.connect() as connection:
        inspector = inspect(connection)
        has_version_table = inspector.has_table("alembic_version")
        has_existing_schema = inspector.has_table("users")

    if has_existing_schema and not has_version_table:
        command.stamp(config, "head")
        return

    command.upgrade(config, "head")


if __name__ == "__main__":
    run_migrations()