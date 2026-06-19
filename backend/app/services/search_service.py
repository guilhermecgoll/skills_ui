import json
import logging
import re

import aiosqlite

from app.config import settings

logger = logging.getLogger(__name__)


def _prepare_fts_query(q: str) -> str | None:
    words = re.findall(r"\w+", q)
    if not words:
        return None
    return " ".join(f'"{w}"*' for w in words)


async def list_skills(
    q: str | None,
    page: int,
    limit: int,
) -> tuple[list[dict], int]:
    offset = (page - 1) * limit

    async with aiosqlite.connect(settings.database_path) as db:
        db.row_factory = aiosqlite.Row
        fts_query = _prepare_fts_query(q) if q else None

        if fts_query:
            try:
                cursor = await db.execute(
                    """
                    SELECT s.slug, s.name, s.description, s.tags, s.author, s.version, s.updated_at
                    FROM skills s
                    WHERE s.slug IN (
                        SELECT slug FROM skills_fts WHERE skills_fts MATCH ?
                        ORDER BY rank
                    )
                    ORDER BY s.name
                    LIMIT ? OFFSET ?
                    """,
                    (fts_query, limit, offset),
                )
                count_cursor = await db.execute(
                    "SELECT COUNT(*) FROM skills_fts WHERE skills_fts MATCH ?",
                    (fts_query,),
                )
            except Exception:
                logger.warning("FTS query failed for %r, falling back to LIKE", q)
                pattern = f"%{q}%"
                cursor = await db.execute(
                    """
                    SELECT slug, name, description, tags, author, version, updated_at
                    FROM skills
                    WHERE name LIKE ? OR description LIKE ?
                    ORDER BY name LIMIT ? OFFSET ?
                    """,
                    (pattern, pattern, limit, offset),
                )
                count_cursor = await db.execute(
                    "SELECT COUNT(*) FROM skills WHERE name LIKE ? OR description LIKE ?",
                    (pattern, pattern),
                )
        else:
            cursor = await db.execute(
                """
                SELECT slug, name, description, tags, author, version, updated_at
                FROM skills ORDER BY name LIMIT ? OFFSET ?
                """,
                (limit, offset),
            )
            count_cursor = await db.execute("SELECT COUNT(*) FROM skills")

        rows = await cursor.fetchall()
        count_row = await count_cursor.fetchone()
        total = count_row[0] if count_row else 0

        result = []
        for row in rows:
            skill = dict(row)
            skill["tags"] = json.loads(skill.get("tags") or "[]")
            result.append(skill)

        return result, total


async def get_skill(slug: str) -> dict | None:
    async with aiosqlite.connect(settings.database_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM skills WHERE slug = ?", (slug,))
        row = await cursor.fetchone()
        if not row:
            return None
        skill = dict(row)
        skill["tags"] = json.loads(skill.get("tags") or "[]")
        return skill
