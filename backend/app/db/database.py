from contextlib import asynccontextmanager
from pathlib import Path

import aiosqlite

from app.config import settings


@asynccontextmanager
async def get_db_connection():
    async with aiosqlite.connect(settings.database_path) as db:
        db.row_factory = aiosqlite.Row
        yield db


async def init_db() -> None:
    db_path = Path(settings.database_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    async with aiosqlite.connect(str(db_path)) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                slug     TEXT PRIMARY KEY,
                name     TEXT NOT NULL,
                description TEXT,
                tags     TEXT,
                author   TEXT,
                version  TEXT,
                content  TEXT,
                updated_at TEXT
            )
        """)

        await db.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS skills_fts USING fts5(
                slug,
                name,
                description,
                tags,
                content_text,
                tokenize = 'unicode61'
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS sync_status (
                id          INTEGER PRIMARY KEY CHECK (id = 1),
                last_sync   TEXT,
                status      TEXT NOT NULL DEFAULT 'never',
                skill_count INTEGER NOT NULL DEFAULT 0
            )
        """)

        await db.execute("""
            INSERT OR IGNORE INTO sync_status (id, last_sync, status, skill_count)
            VALUES (1, NULL, 'never', 0)
        """)

        await db.commit()


async def get_sync_status() -> dict:
    async with aiosqlite.connect(settings.database_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT last_sync, status, skill_count FROM sync_status WHERE id = 1"
        )
        row = await cursor.fetchone()
        if not row:
            return {"last_sync": None, "status": "never", "skill_count": 0}
        return dict(row)
