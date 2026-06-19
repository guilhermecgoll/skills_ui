import logging

from fastapi import APIRouter, HTTPException

from app.db.database import get_sync_status
from app.services import git_service, indexer

router = APIRouter(prefix="/sync", tags=["sync"])
logger = logging.getLogger(__name__)


@router.get("/status")
async def status():
    return await get_sync_status()


@router.post("/trigger")
async def trigger():
    try:
        await git_service.sync_repo()
    except Exception as exc:
        logger.error("Git sync failed: %s", exc)
        raise HTTPException(status_code=500, detail=f"Git sync failed: {exc}")

    count = await indexer.reindex()
    sync_status = await get_sync_status()
    return {"message": "Sync completed", "skill_count": count, **sync_status}
