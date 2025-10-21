"""
FastAPI application with reorganized structure
Main entry point that registers API services: data_service, ai_service, ai_analytics_service, and health_service
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import logging
import os

from ..config.settings import config_manager
from ..handler.financial_handler import FinancialDataHandler
from ..models.financial_models import QueryRequest, QueryResponse

# Import the main API services
from .services.data_service import router as data_router
from .services.ai_service import router as ai_router
from .services.ai_analytics_service import router as ai_analytics_router
from .services.health_service import router as health_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Financial Data Processing System",
    description="AI-powered financial data analysis and natural language querying with organized service architecture",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
financial_service = FinancialDataHandler()

# Register the main API services
app.include_router(data_router)
app.include_router(ai_router)
app.include_router(ai_analytics_router)
app.include_router(health_router)


# ROOT ENDPOINT
@app.get("/")
async def root():
    """Root endpoint with API information"""
    config = config_manager.config
    return {
        "message": "Financial Data Processing System",
        "version": "1.0.0",
        "environment": config.environment.value,
        "database_type": config.database.type,
        "architecture": "Organized service architecture with multiple specialized services",
        "services": {
            "data_service": {
                "description": "Handles data operations: sync, list, summary, aggregate",
                "endpoints": {
                    "sync": "/api/data/sync",
                    "list": "/api/data/list",
                    "summary": "/api/data/summary",
                    "aggregate": "/api/data/aggregate",
                    "search": "/api/data/search",
                    "periods": "/api/data/periods",
                },
            },
            "ai_service": {
                "description": "Handles AI query operations",
                "endpoints": {"query": "/api/ai/query"},
            },
            "ai_analytics_service": {
                "description": "Handles AI-powered financial analytics",
                "endpoints": {
                    "analytics_comprehensive": "/api/ai/analytics/comprehensive",
                    "analytics_trends": "/api/ai/analytics/trends",
                    "analytics_anomalies": "/api/ai/analytics/anomalies",
                    "analytics_health_score": "/api/ai/analytics/health-score",
                },
            },
            "health_service": {
                "description": "Handles basic health checks",
                "endpoints": {"basic": "/api/health/"},
            },
        },
    }


# LEGACY ENDPOINTS (for backward compatibility)
@app.post("/query", response_model=QueryResponse)
async def legacy_process_natural_language_query(request: QueryRequest):
    """Legacy endpoint - redirects to AI service"""
    try:
        # Initialize AI service for legacy compatibility (Azure OpenAI only)
        from ..handler.ai.ai_query_service import AIQueryService

        llm_model = os.getenv("LLM_MODEL")  # Azure deployment name
        llm_temperature = float(os.getenv("LLM_TEMPERATURE", "0.4"))

        ai_query_service = AIQueryService(
            financial_service, llm_model=llm_model, llm_temperature=llm_temperature
        )

        response = ai_query_service.process_query(request.query)
        response.note = "This is a legacy endpoint. Use /api/ai/query for the new API."
        return response
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="Error processing query")


if __name__ == "__main__":
    import uvicorn

    config = config_manager.config
    uvicorn.run(
        app,
        host=config.api.host,
        port=config.api.port,
        reload=config.api.reload,
        log_level=config.log_level.lower(),
    )
