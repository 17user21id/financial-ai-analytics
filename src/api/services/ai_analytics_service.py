"""
AI Analytics Service API
Handles AI-powered financial analytics endpoints
"""

from fastapi import APIRouter, HTTPException, Query
import logging

from ...handler.ai.analytics_service import AdvancedAnalyticsService
import os

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/ai", tags=["ai-analytics"])


def get_analytics_service():
    """Get analytics service singleton instance"""
    try:
        llm_model = os.getenv("LLM_MODEL")
        llm_temperature = float(os.getenv("LLM_TEMPERATURE", "0.4"))

        return AdvancedAnalyticsService.get_instance(
            llm_provider="azure", llm_model=llm_model, llm_temperature=llm_temperature
        )
    except Exception as e:
        logger.error(f"Failed to initialize analytics service: {e}")
        raise HTTPException(
            status_code=500, detail=f"Analytics service unavailable: {str(e)}"
        )


# AI ANALYTICS ENDPOINTS
@router.get("/analytics/comprehensive")
async def get_comprehensive_analysis(
    period_start: str = Query(None, description="Start date (YYYY-MM-DD)"),
    period_end: str = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get comprehensive AI-powered financial analysis"""
    try:
        analytics_service = get_analytics_service()
        analysis = analytics_service.get_comprehensive_analysis(
            period_start, period_end
        )
        return analysis
    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/trends")
async def get_trend_analysis(
    period_start: str = Query(None, description="Start date (YYYY-MM-DD)"),
    period_end: str = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get AI-powered trend analysis"""
    try:
        analytics_service = get_analytics_service()
        trends = analytics_service.get_trend_analysis(period_start, period_end)
        return trends
    except Exception as e:
        logger.error(f"Error in trend analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/anomalies")
async def get_anomaly_detection(
    period_start: str = Query(None, description="Start date (YYYY-MM-DD)"),
    period_end: str = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get AI-powered anomaly detection"""
    try:
        analytics_service = get_analytics_service()
        anomalies = analytics_service.get_anomaly_detection(period_start, period_end)
        return anomalies
    except Exception as e:
        logger.error(f"Error in anomaly detection: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/health-score")
async def get_financial_health_score(
    period_start: str = Query(None, description="Start date (YYYY-MM-DD)"),
    period_end: str = Query(None, description="End date (YYYY-MM-DD)"),
):
    """Get AI-powered financial health score"""
    try:
        analytics_service = get_analytics_service()
        health_score = analytics_service.get_health_score(period_start, period_end)
        return health_score
    except Exception as e:
        logger.error(f"Error in health scoring: {e}")
        raise HTTPException(status_code=500, detail=str(e))
