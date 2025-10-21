"""
Data Service API
Handles all data-related operations: sync, list, summary, aggregate
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Dict, Any
import logging

from ...handler.financial_handler import FinancialDataHandler
from ...handler.data_sync_handler import DataSyncHandler
from ...stores.database_manager import get_database_manager
from ...common.enum_converter import enum_converter
from ...common.enums import AccountType
from ...models.financial_models import GroupedMetricsRequest, GroupedMetricsResponse
from ...models.query_models import (
    TransactionResponse,
    TransactionListResponse,
    TransactionQueryRequest,
    EnhancedAggregateRequest,
    EnhancedAggregateResponse,
    SyncResponse,
)

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/data", tags=["data"])

# Initialize service
financial_handler = FinancialDataHandler()
data_sync_handler = DataSyncHandler()


# SYNC ENDPOINTS
@router.post("/sync", response_model=SyncResponse)
async def sync_data():
    """
    Synchronously sync data from Excel files to accounts and transactions tables

    Automatically finds and processes:
    - dataset1_output_*.xlsx (P&L Report)
    - dataset2_output_*.xlsx (Rootfi Report)

    Returns:
        SyncResponse with sync results
    """
    try:
        return data_sync_handler.sync_excel_data()
    except Exception as e:
        logger.error(f"Error in Excel data sync: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/list", response_model=TransactionListResponse)
async def list_transactions(
    request: TransactionQueryRequest,
    language: str = Query("en", description="Language code for localization"),
    db=Depends(get_database_manager),
):
    """
    List financial transactions with advanced filtering capabilities
    """
    try:
        # Convert FilterCondition objects to dictionaries
        parsed_filters = []
        if request.filters:
            for filter_condition in request.filters:
                field = filter_condition.field
                value = filter_condition.value

                if field and value is not None:
                    # Convert enum values
                    converted_value = enum_converter.convert_filter_value(field, value)
                    parsed_filters.append(
                        {
                            "field": field,
                            "operator": filter_condition.operator,
                            "value": converted_value,
                        }
                    )

        # Query database
        result = db.transaction_store.query_transactions(
            filters=parsed_filters,
            order_by=request.order_by,
            limit=request.limit,
            offset=request.offset,
            language=language,
        )

        return TransactionListResponse(**result)

    except Exception as e:
        logger.error(f"Error in list_transactions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list/{tx_id}", response_model=TransactionResponse)
async def get_transaction(
    tx_id: int,
    language: str = Query("en", description="Language code for localization"),
    db=Depends(get_database_manager),
):
    """Get a specific transaction by ID"""
    try:
        # Query for specific transaction
        result = db.query_transactions(
            filters=[{"field": "tx_id", "operator": "=", "value": tx_id}],
            limit=1,
            language=language,
        )

        if not result["data"]:
            raise HTTPException(status_code=404, detail="Transaction not found")

        return TransactionResponse(**result["data"][0])

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_transaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# AGGREGATE ENDPOINTS
@router.post("/aggregate", response_model=EnhancedAggregateResponse)
async def get_enhanced_transaction_aggregate(
    request: EnhancedAggregateRequest,
    language: str = Query("en", description="Language code for localization"),
    db=Depends(get_database_manager),
):
    """Get enhanced aggregated financial transaction data with type filtering and calculated fields"""
    try:
        # Convert FilterCondition objects to dictionaries
        parsed_filters = []
        if request.filters:
            for filter_condition in request.filters:
                field = filter_condition.field
                operator = filter_condition.operator
                value = filter_condition.value

                if field and value is not None:
                    # Convert enum fields using the same logic as list API
                    converted_value = enum_converter.convert_filter_value(field, value)
                    parsed_filters.append(
                        {"field": field, "operator": operator, "value": converted_value}
                    )

        # Add account type filter if specified
        if request.account_types:
            account_type_values = [
                enum_converter.convert_filter_value("account_type", t)
                for t in request.account_types
            ]
            if account_type_values:
                parsed_filters.append(
                    {
                        "field": "account_type",
                        "operator": "IN",
                        "value": account_type_values,
                    }
                )

        # Add period filter if specified
        if request.period_start:
            parsed_filters.append(
                {
                    "field": "period_start",
                    "operator": ">=",
                    "value": request.period_start,
                }
            )

        if request.period_end:
            parsed_filters.append(
                {"field": "period_end", "operator": "<=", "value": request.period_end}
            )

        # Convert AggregateFunction objects to dictionaries
        parsed_aggregates = []
        if request.aggregates:
            for agg_func in request.aggregates:
                parsed_aggregates.append(
                    {
                        "function": agg_func.function,
                        "field": agg_func.field,
                        "alias": agg_func.alias,
                    }
                )
        else:
            # Default aggregation
            parsed_aggregates.append(
                {"function": "SUM", "field": "value", "alias": "total_value"}
            )

        # Enhanced group_by processing for period grouping
        enhanced_group_by = []
        if request.group_by:
            for group_field in request.group_by:
                if group_field in ["month", "quarter", "year"]:
                    # Add period-based grouping
                    if group_field == "month":
                        enhanced_group_by.append("strftime('%Y-%m', ft.period_start)")
                    elif group_field == "quarter":
                        enhanced_group_by.append(
                            "strftime('%Y', ft.period_start) || '-Q' || CASE WHEN CAST(strftime('%m', ft.period_start) AS INTEGER) BETWEEN 1 AND 3 THEN '1' WHEN CAST(strftime('%m', ft.period_start) AS INTEGER) BETWEEN 4 AND 6 THEN '2' WHEN CAST(strftime('%m', ft.period_start) AS INTEGER) BETWEEN 7 AND 9 THEN '3' ELSE '4' END"
                        )
                    elif group_field == "year":
                        enhanced_group_by.append("strftime('%Y', ft.period_start)")
                else:
                    # Regular field grouping
                    enhanced_group_by.append(group_field)
        else:
            enhanced_group_by = request.group_by

        # Use the enhanced aggregate query method
        result = db.query_transactions_aggregate(
            filters=parsed_filters,
            group_by=enhanced_group_by,
            aggregates=parsed_aggregates,
            order_by=request.order_by,
            limit=request.limit,
            offset=request.offset,
            language=language,
        )

        # Calculate derived metrics if requested
        calculated_fields = None
        if request.calculate_derived:
            calculated_fields = _calculate_derived_metrics_from_groups(result["groups"])

        # Create enhanced response
        enhanced_result = {
            **result,
            "account_type_filter": request.account_types,
            "calculated_fields": calculated_fields,
            "period_filter": (
                {"start": request.period_start, "end": request.period_end}
                if request.period_start or request.period_end
                else None
            ),
        }

        return EnhancedAggregateResponse(**enhanced_result)

    except Exception as e:
        logger.error(f"Error in get_enhanced_transaction_aggregate: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _calculate_derived_metrics_from_groups(
    groups: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Calculate derived metrics from grouped data"""
    total_revenue = 0
    total_cogs = 0
    total_expenses = 0
    total_tax = 0

    for group in groups:
        # Extract values based on account type or group key
        if "account_type" in group:
            account_type = group.get("account_type")
            value = group.get("total_value", 0)

            if account_type == 1:  # revenue
                total_revenue += value
            elif account_type == 2:  # cogs
                total_cogs += value
            elif account_type == 3:  # expense
                total_expenses += value
            elif account_type == 4:  # tax
                total_tax += value

    return {
        "gross_profit": total_revenue - total_cogs,
        "operating_profit": total_revenue - total_cogs - total_expenses,
        "net_profit": total_revenue - total_cogs - total_expenses - total_tax,
        "gross_margin_percent": (
            (total_revenue - total_cogs) / total_revenue * 100
            if total_revenue > 0
            else 0
        ),
        "operating_margin_percent": (
            (total_revenue - total_cogs - total_expenses) / total_revenue * 100
            if total_revenue > 0
            else 0
        ),
        "net_margin_percent": (
            (total_revenue - total_cogs - total_expenses - total_tax)
            / total_revenue
            * 100
            if total_revenue > 0
            else 0
        ),
        "total_revenue": total_revenue,
        "total_cogs": total_cogs,
        "total_expenses": total_expenses,
        "total_tax": total_tax,
    }


@router.post("/grouped-metrics", response_model=List[GroupedMetricsResponse])
async def get_grouped_metrics(request: GroupedMetricsRequest):
    """Get grouped/aggregated financial metrics with filters"""
    try:
        logger.info(
            f"Processing grouped metrics request: group_by={request.group_by}, filters={len(request.filters) if request.filters else 0}"
        )

        # Convert FilterRequest objects to dictionaries
        filters_dict = []
        if request.filters:
            for filter_req in request.filters:
                filters_dict.append(
                    {
                        "field": filter_req.field,
                        "operator": filter_req.operator,
                        "value": filter_req.value,
                        "value_list": filter_req.value_list,
                    }
                )

        # Get grouped metrics from service
        results = financial_handler.get_grouped_metrics(
            group_by=request.group_by,
            filters=filters_dict,
            aggregation=request.aggregation,
            limit=request.limit,
        )

        # Convert to response objects
        response_objects = []
        for result in results:
            response_objects.append(
                GroupedMetricsResponse(
                    group_value=result["group_value"],
                    aggregation_type=result["aggregation_type"],
                    aggregated_value=result["aggregated_value"],
                    record_count=result["record_count"],
                    group_by_field=result["group_by_field"],
                )
            )

        logger.info(f"Returning {len(response_objects)} grouped metrics")
        return response_objects

    except ValueError as e:
        logger.error(f"Validation error in grouped metrics request: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing grouped metrics request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# UTILITY ENDPOINTS
@router.get("/periods")
async def get_available_periods():
    """Get all available time periods in the database"""
    periods = financial_handler.get_available_periods()
    return {"periods": periods, "count": len(periods)}


@router.get("/metrics/{account_type}")
async def get_metrics_by_type(
    account_type: str, limit: int = Query(100, description="Maximum number of results")
):
    """Get financial metrics by account type"""
    valid_types = [
        "revenue",
        "cogs",
        "operating_expense",
        "non_operating_revenue",
        "non_operating_expense",
        "tax",
        "derived",
    ]

    if account_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid account type. Must be one of: {valid_types}",
        )

    metrics = financial_handler.get_metrics_by_type(account_type, limit)
    return {"account_type": account_type, "count": len(metrics), "data": metrics}
