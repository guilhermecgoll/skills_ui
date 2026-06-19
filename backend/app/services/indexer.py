import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path

import frontmatter

from app.config import settings
from app.db.database import get_db_connection

logger = logging.getLogger(__name__)


def _name_from_slug(slug: str) -> str:
    return re.sub(r"[-_]+", " ", slug).strip().title()


def _first_paragraph(content: str) -> str:
    for line in content.strip().splitlines():
        line = line.strip().lstrip("#").strip()
        if line:
            return line[:300]
    return ""


def _parse_skill(skill_dir: Path) -> dict | None:
    skill_md = skill_dir / "skill.md"
    if not skill_md.exists():
        return None

    try:
        post = frontmatter.load(str(skill_md))
    except Exception as exc:
        logger.warning("Could not parse %s: %s", skill_md, exc)
        return None

    slug = skill_dir.name
    name = post.get("name") or _name_from_slug(slug)
    description = post.get("description") or _first_paragraph(post.content)

    tags = post.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]

    return {
        "slug": slug,
        "name": str(name),
        "description": str(description),
        "tags": json.dumps(tags),
        "author": str(post.get("author") or ""),
        "version": str(post.get("version") or ""),
        "content": post.content,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


async def reindex() -> int:
    repo_path = Path(settings.repo_local_path)
    if not repo_path.exists():
        logger.warning("Repo path %s does not exist — skipping index", repo_path)
        return 0

    skills: list[dict] = []
    for skill_dir in sorted(repo_path.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        skill = _parse_skill(skill_dir)
        if skill:
            skills.append(skill)

    async with get_db_connection() as db:
        await db.execute("DELETE FROM skills_fts")
        await db.execute("DELETE FROM skills")

        for skill in skills:
            await db.execute(
                """
                INSERT INTO skills (slug, name, description, tags, author, version, content, updated_at)
                VALUES (:slug, :name, :description, :tags, :author, :version, :content, :updated_at)
                """,
                skill,
            )
            await db.execute(
                """
                INSERT INTO skills_fts (slug, name, description, tags, content_text)
                VALUES (:slug, :name, :description, :tags, :content)
                """,
                skill,
            )

        await db.execute(
            """
            UPDATE sync_status
            SET last_sync = ?, status = 'ok', skill_count = ?
            WHERE id = 1
            """,
            (datetime.now(timezone.utc).isoformat(), len(skills)),
        )
        await db.commit()

    logger.info("Indexed %d skill(s)", len(skills))
    return len(skills)
