from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/set_alembic_version.py <revision_id>")

    revision_id = sys.argv[1].strip()
    if not revision_id:
        raise SystemExit("revision_id is empty")

    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL is missing. Create backend/.env first.")

    engine = create_engine(database_url)

    with engine.begin() as conn:
        # Ensure table exists
        conn.execute(
            text(
                "create table if not exists alembic_version (version_num varchar(32) not null)"
            )
        )

        rows = conn.execute(text("select count(*) from alembic_version")).scalar() or 0
        if rows == 0:
            conn.execute(
                text("insert into alembic_version(version_num) values (:v)"),
                {"v": revision_id},
            )
        else:
            conn.execute(text("update alembic_version set version_num=:v"), {"v": revision_id})

    print(f"Set alembic_version to {revision_id}")


if __name__ == "__main__":
    main()
