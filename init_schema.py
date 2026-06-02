from pathlib import Path
import os

import psycopg2


def _make_idempotent(statement: str) -> str:
    normalized = statement.lstrip()
    if normalized.upper().startswith("CREATE TABLE "):
        return statement.replace("CREATE TABLE ", "CREATE TABLE IF NOT EXISTS ", 1)
    if normalized.upper().startswith("CREATE INDEX "):
        return statement.replace("CREATE INDEX ", "CREATE INDEX IF NOT EXISTS ", 1)
    return statement

"""
def main() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL is required")

    # Prefer tracked schema path; fall back to memo/database/tables.sql if present
    tracked = Path(__file__).resolve().parent / "schema" / "tables.sql"
    fallback = Path(__file__).resolve().parent / "memo" / "database" / "tables.sql"
    if tracked.exists():
        sql_path = tracked
    elif fallback.exists():
        sql_path = fallback
    else:
        raise SystemExit("No schema file found (looked for schema/tables.sql and memo/database/tables.sql)")

    sql_text = sql_path.read_text(encoding="utf-8")

    statements = [statement.strip() for statement in sql_text.split(";") if statement.strip()]

    with psycopg2.connect(database_url) as conn:
        with conn.cursor() as cur:
            for statement in statements:
                cur.execute(_make_idempotent(statement))

    print(f"Executed {len(statements)} SQL statements from {sql_path}")


if __name__ == "__main__":
    main()
"""