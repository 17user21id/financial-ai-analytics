"""
AI Service API
Handles AI query operations
"""

from fastapi import APIRouter, HTTPException, Query
import logging
from datetime import datetime

from ...handler.ai_handler import get_ai_handler
from ...common.system_logger import system_logger
from ...models.query_models import (
    AIQueryRequest,
    AIQueryResponse,
    AIInteractionType,
    AIArchitectureMode,
)

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/ai", tags=["ai"])

# Default interaction type: DB (database-based SQL generation)
default_interaction_type = AIInteractionType.DB


# AI QUERY ENDPOINTS
@router.post("/query", response_model=AIQueryResponse)
async def process_ai_query(
    request: AIQueryRequest,
    use_v2: bool = Query(True, description="Use Two-API architecture (v2)"),
):
    """
    Process natural language query using advanced AI (defaults to V2 architecture)

    Query Parameters:
    - use_v2: If true (default), use Two-API architecture (SQL generation + formatting)
              If false, use standard single-API approach
    """
    query_start_time = datetime.now()

    try:
        # Set interaction type and architecture mode (V2 is now default)
        interaction_type = default_interaction_type  # Currently: DB-based interaction
        architecture_mode = AIArchitectureMode.V2 if use_v2 else AIArchitectureMode.V1

        system_logger.api_info(
            f"Processing AI query: {request.query[:50]}...",
            {
                "query_length": len(request.query),
                "endpoint": "/api/ai/query",
                "architecture": architecture_mode,
                "interaction_type": interaction_type,
            },
        )

        # Get AI handler and process query with database-based interaction
        ai_handler = get_ai_handler()
        query_response = ai_handler.process_query(
            query=request.query,
            chat_id=request.chat_id,
            user_id=request.user_id,
            use_v2=use_v2,
        )

        query_response_time = (datetime.now() - query_start_time).total_seconds()
        system_logger.log_api_request(
            method="POST",
            endpoint="/api/ai/query",
            status_code=200,
            response_time=query_response_time,
            extra={
                "query": request.query,
                "response_length": len(query_response.answer),
                "confidence": query_response.confidence,
                "interaction_type": interaction_type,
                "architecture": architecture_mode,
            },
        )

        return AIQueryResponse(
            query=query_response.query,
            answer=query_response.answer,
            confidence=query_response.confidence,
            data_points=query_response.data_points,
            insights=query_response.insights,
            timestamp=query_response.timestamp,
            chat_id=query_response.chat_id,
        )

    except Exception as e:
        error_response_time = (datetime.now() - query_start_time).total_seconds()
        system_logger.api_error(
            f"Error processing AI query: {e}",
            {
                "query": request.query,
                "response_time": error_response_time,
                "interaction_type": default_interaction_type,
            },
        )
        raise HTTPException(status_code=500, detail=str(e))
