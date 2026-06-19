import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import scheduler
from app.api.routes import skills, sync
from app.db.database import init_db
from app.services import git_service, indexer

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s — %(message)s")
logger = logging.getLogger(__name__)


async def _initial_sync() -> None:
    try:
        await git_service.sync_repo()
        await indexer.reindex()
    except Exception as exc:
        logger.error("Initial sync failed: %s", exc)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    asyncio.create_task(_initial_sync())
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(title="Skills UI API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(skills.router, prefix="/api")
app.include_router(sync.router, prefix="/api")
