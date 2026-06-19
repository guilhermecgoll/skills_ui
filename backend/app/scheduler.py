import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import settings
from app.services import git_service, indexer

logger = logging.getLogger(__name__)
_scheduler = AsyncIOScheduler()


async def _sync_job() -> None:
    logger.info("Scheduled sync started")
    try:
        await git_service.sync_repo()
        count = await indexer.reindex()
        logger.info("Scheduled sync completed: %d skill(s)", count)
    except Exception as exc:
        logger.error("Scheduled sync failed: %s", exc)


def start() -> None:
    _scheduler.add_job(
        _sync_job,
        "interval",
        minutes=settings.sync_interval_minutes,
        id="sync_repo",
        replace_existing=True,
    )
    _scheduler.start()
    logger.info("Scheduler started — interval: %d min", settings.sync_interval_minutes)


def shutdown() -> None:
    _scheduler.shutdown(wait=False)
