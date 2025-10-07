from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/", tags=["Health"], summary="Check server status", response_description="Information about server status")
async def health_check():
    """
    Health Check Endpoint

    This endpoint responds to a GET request at the root URL `/`. 
    Main purposes:
    - Check API availability;
    - Simple health check for server monitoring;
    - Confirm that the FastAPI application is running and ready to accept requests.

    Response:
    - JSON with a message about server status and API version.
    """
    return {
        "status": "OK",
        "message": f"{settings.PROJECT_NAME} is running ᕙ(⇀‸↼‵‵)ᕗ",
        "version": settings.VERSION
    }
