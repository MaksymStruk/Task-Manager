import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from app.log.custom_logger import custom_logger as logger

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Manager API"
    DESCRIPTION: str = "API для керування задачами з відкладеним виконанням"
    VERSION: str = "0.0.1"
    DEBUG: bool = True

    DATABASE_URL: str = os.getenv("DATABASE_URL","sqlite:///./taskmanager.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))

    class Config:
        env_file = ".env"

settings = Settings()
