from fastapi import FastAPI
from datetime import datetime
from contextlib import asynccontextmanager
from app.log.custom_logger import logger_test, custom_logger as logger
from app.db.database import engine, get_db_session, Base
from app.routers.v1 import server, task
from app.services.task_service import TaskService
from app.core.config import settings
from app.core.ascii_art import ASCII_ART
from app.core.middleware import setup_middlewares

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    if settings.DEBUG:
        logger_test()
    logger.info(f"[Startup] {settings.PROJECT_NAME} {settings.VERSION} started")
    db = next(get_db_session())
    service = TaskService(db)
    updated_count = service.mark_overdue_tasks_done()
    logger.info(f"[Startup] Marked {updated_count} overdue tasks as DONE")
    db.close()

    logger.success(f"Server started at {datetime.now()}\n{ASCII_ART}")

    yield

    # --- shutdown ---
    logger.info("[Shutdown] FastAPI server is stopping...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan
)

# Enable CORS
setup_middlewares(app)

app.include_router(server.router)
app.include_router(task.router, prefix="/api/v1")
