from __future__ import annotations

import os
from pathlib import Path

from alembic import command
from alembic.config import Config


def run_migrations() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL is required")

    alembic_ini = Path(__file__).resolve().parent / "alembic.ini"
    if not alembic_ini.exists():
        raise SystemExit(f"Alembic configuration not found: {alembic_ini}")

    config = Config(str(alembic_ini))
    config.set_main_option("sqlalchemy.url", database_url)
    command.upgrade(config, "head")


if __name__ == "__main__":
    run_migrations()