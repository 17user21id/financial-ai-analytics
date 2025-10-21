"""
API Services Package
Contains the four main API services: data_service, ai_service, ai_analytics_service, and health_service
"""

from .data_service import router as data_router
from .ai_service import router as ai_router
from .ai_analytics_service import router as ai_analytics_router
from .health_service import router as health_router

__all__ = ["data_router", "ai_router", "ai_analytics_router", "health_router"]
