import asyncio
import logging
from pathlib import Path

from git import GitCommandError, InvalidGitRepositoryError, Repo

from app.config import settings

logger = logging.getLogger(__name__)


def _sync_blocking(repo_path: Path) -> None:
    if not (repo_path / ".git").exists():
        repo_path.mkdir(parents=True, exist_ok=True)
        logger.info("Cloning %s → %s", settings.skills_repo_url, repo_path)
        Repo.clone_from(settings.skills_repo_url, str(repo_path))
    else:
        logger.info("Pulling latest changes in %s", repo_path)
        try:
            repo = Repo(str(repo_path))
            repo.remotes.origin.pull()
        except InvalidGitRepositoryError:
            logger.warning("Invalid repo at %s — re-cloning", repo_path)
            import shutil
            shutil.rmtree(repo_path)
            repo_path.mkdir(parents=True, exist_ok=True)
            Repo.clone_from(settings.skills_repo_url, str(repo_path))


async def sync_repo() -> None:
    repo_path = Path(settings.repo_local_path)
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, _sync_blocking, repo_path)
    except GitCommandError as exc:
        logger.error("Git sync failed: %s", exc)
        raise
