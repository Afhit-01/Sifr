from datetime import datetime, timezone

from fastapi import APIRouter

from app.config import get_settings
from app.logger import get_logger

router = APIRouter(tags=["Health"])
logger = get_logger(__name__)
settings = get_settings()


@router.get("/health")
def health_check():
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/ready")
def readiness_check():
    logger.info("Readiness check requested")
    return {
        "status": "ready",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
