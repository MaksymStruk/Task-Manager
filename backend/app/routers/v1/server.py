from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(
    tags=['Server']
)

@router.get("/")
async def root():
    """API root endpoint.

    Returns basic information about the Task Manager API.

    Returns:
        dict: API information including:
            - message: Welcome message
            - version: API version
            - status: Server status

    Example:
        GET /

    Response:
        {
            "status": "OK",
            "message": "Task Manager API is running",
            "version": "1.0.0"
        }
    """
    return {
        "status": "OK",
        "message": f"{settings.PROJECT_NAME} is running (˶ᵔ ᵕ ᵔ˶)",
        "version": settings.VERSION
    }


@router.get("/health")
async def health_check():
    """Health check endpoint.

    Check if the API server is running and healthy. This endpoint is typically
    used by monitoring systems and load balancers.

    Returns:
        dict: Health status information including:
            - status: Overall health status
            - timestamp: Current server time
            - uptime: Server uptime information

    Example:
        GET /health

    Response:
        {
            "status": "healthy",
            "timestamp": "2025-01-07T10:30:00Z",
            "uptime": "2h 15m 30s"
        }
    """
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "API is running normally (˶ˆᗜˆ˵)"
    }
