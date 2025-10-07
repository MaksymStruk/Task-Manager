"""FastAPI application main module.

This module creates and configures the FastAPI application with
async database initialization, middleware setup, and route registration.
"""

from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.log.custom_logger import logger_test, custom_logger as logger
from app.db.database import Base, AsyncSessionLocal, async_engine
from app.routers.v1 import server, task
from app.services.task_service import TaskService
from app.core.config import settings
from app.core.ascii_art import ASCII_ART
from app.core.middleware import setup_middlewares

# --- Async database initialization ---
async def init_db():
    """Initialize database tables asynchronously."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("[Startup] Database tables created")

# --- FastAPI lifespan management ---
@asynccontextmanager
async def lifespan(application: FastAPI):
    """Manage application startup and shutdown lifecycle.

    Args:
        application: FastAPI application instance

    Yields:
        None: Control back to FastAPI during runtime
    """
    # --- startup ---
    if settings.DEBUG:
        logger_test()
    logger.info(f"[Startup] {settings.PROJECT_NAME} {settings.VERSION} starting...")

    # Initialize database tables
    await init_db()

    # Mark overdue tasks as DONE
    async with AsyncSessionLocal() as db:
        service = TaskService(db)
        updated_count = await service.mark_overdue_tasks_done()
        logger.info(f"[Startup] Marked {updated_count} overdue tasks as DONE")

    logger.success(f"[Startup] Server started at {datetime.now()}\n{ASCII_ART}")

    yield  # FastAPI handles requests here

    # --- shutdown ---
    logger.info("[Shutdown] FastAPI server is stopping...")

# --- FastAPI application initialization ---
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan
)

# Enable CORS and other middleware
setup_middlewares(app)

# --- Route registration ---
app.include_router(server.router)
app.include_router(task.router, prefix="/api/v1")
