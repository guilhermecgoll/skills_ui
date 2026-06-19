import io
import re
import zipfile
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.config import settings
from app.services import search_service

router = APIRouter(prefix="/skills", tags=["skills"])

_VALID_SLUG = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]*$")


def _validate_slug(slug: str) -> None:
    if not _VALID_SLUG.match(slug):
        raise HTTPException(status_code=400, detail="Invalid skill name")


@router.get("")
async def list_skills(
    q: str | None = Query(None, description="Full-text search query"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    skills, total = await search_service.list_skills(q or None, page, limit)
    return {
        "items": skills,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": max(1, (total + limit - 1) // limit),
    }


@router.get("/{slug}")
async def get_skill(slug: str):
    _validate_slug(slug)
    skill = await search_service.get_skill(slug)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@router.get("/{slug}/download")
async def download_skill(slug: str):
    _validate_slug(slug)

    skill_path = Path(settings.repo_local_path) / slug
    if not skill_path.is_dir():
        raise HTTPException(status_code=404, detail="Skill not found")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in skill_path.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(skill_path.parent))
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{slug}.zip"'},
    )
