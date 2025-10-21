"""
Health Service API
Handles basic health checks
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from datetime import datetime

from ...config.settings import config_manager

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/health", tags=["health"])


# Pydantic models for API
class HealthStatus(BaseModel):
    """Health status response model"""

    status: str
    timestamp: str
    environment: str
    database_type: str


# BASIC HEALTH ENDPOINTS
@router.get("/", response_model=HealthStatus)
async def health_check():
    """Basic health check endpoint"""
    config = config_manager.config
    return HealthStatus(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        environment=config.environment.value,
        database_type=config.database.type,
    )


@router.get("/basic")
async def basic_health():
    """Basic health check with minimal information"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "Service is running",
    }
