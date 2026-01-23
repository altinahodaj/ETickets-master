from __future__ import annotations

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def main() -> None:
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL is missing. Create backend/.env first.")

    engine = create_engine(database_url)

    with engine.connect() as conn:
        try:
            version = conn.execute(text("select version_num from alembic_version")).scalar()
        except Exception as exc:  # alembic_version might not exist yet
            version = None
            print(f"alembic_version: <missing> ({exc.__class__.__name__})")
        else:
            print(f"alembic_version: {version}")

        tables = conn.execute(
            text("select tablename from pg_tables where schemaname='public' order by tablename")
        ).fetchall()
        print("tables:", [t[0] for t in tables])


if __name__ == "__main__":
    main()
