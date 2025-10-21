from dataclasses import dataclass
from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel, Field
from enum import Enum, auto


# AI Service Models
class AIInteractionType(Enum):
    """
    AI Interaction Types

    DB: Database-based interaction (SQL generation + execution)
    AGENT: Agent-based interaction (function calling, reasoning, tool usage)
    """

    DB = auto()
    AGENT = auto()


class AIArchitectureMode(Enum):
    """
    AI Architecture Modes

    V1: Version 1 - Single-API approach (one LLM call for query processing)
    V2: Version 2 - Two-API approach (separate SQL generation and formatting calls)
    """

    V1 = auto()
    V2 = auto()


class AIQueryRequest(BaseModel):
    """Request model for AI queries"""

    query: str = Field(..., description="Natural language query about financial data")
    chat_id: Optional[str] = Field(
        None, description="Chat session ID for context-aware conversations"
    )
    user_id: Optional[str] = Field(None, description="User ID for personalization")

    class Config:
        schema_extra = {
            "example": {
                "query": "What is the total revenue for this quarter?",
                "chat_id": "chat_20250119_123456_user123",
                "user_id": "user123",
            }
        }


class AIQueryResponse(BaseModel):
    """Response model for AI queries"""

    query: str
    answer: str
    confidence: float
    data_points: Optional[List[Dict[str, Any]]] = None
    insights: Optional[List[str]] = None
    timestamp: str
    chat_id: Optional[str] = None


# Data Service Models
class FilterCondition(BaseModel):
    """Single filter condition"""

    field: str = Field(..., description="Field name to filter on")
    operator: str = Field(default="=", description="Filter operator")
    value: Union[str, int, float, List[Union[str, int, float]]] = Field(
        ..., description="Filter value"
    )


class TransactionResponse(BaseModel):
    """Transaction response model"""

    tx_id: int
    account_id: int
    account_name: str
    account_type: int
    account_type_localized: Optional[str] = None
    sub_type: Optional[int] = None
    sub_type_localized: Optional[str] = None
    is_derived: bool
    description: Optional[str] = None
    period_start: str
    period_end: str
    value: float
    currency: int
    currency_localized: Optional[str] = None
    derived_sub_type: Optional[int] = None
    derived_sub_type_localized: Optional[str] = None
    posted_date: Optional[str] = None
    created_by: Optional[str] = None
    notes: Optional[str] = None
    source_id: int
    source_id_localized: Optional[str] = None


class TransactionListResponse(BaseModel):
    """Transaction list response model"""

    data: List[TransactionResponse]
    total_count: int
    limit: Optional[int] = None
    offset: Optional[int] = None
    has_more: bool


class TransactionQueryRequest(BaseModel):
    """Request model for transaction queries"""

    filters: Optional[List[FilterCondition]] = Field(
        default=None, description="List of filter conditions"
    )
    order_by: Optional[str] = Field(
        default=None, description="Field to order by (e.g., 'value DESC')"
    )
    limit: Optional[int] = Field(
        default=100, ge=1, le=1000, description="Maximum number of records to return"
    )
    offset: Optional[int] = Field(
        default=0, ge=0, description="Number of records to skip"
    )


class AggregateFunction(BaseModel):
    """Aggregate function specification"""

    function: str = Field(
        ..., description="Aggregate function: SUM, COUNT, AVG, MIN, MAX"
    )
    field: str = Field(
        ..., description="Field to aggregate on (e.g., 'value', 'tx_id')"
    )
    alias: Optional[str] = Field(
        default=None, description="Alias for the aggregated result"
    )


class TransactionAggregateRequest(BaseModel):
    """Request model for transaction aggregate queries"""

    filters: Optional[List[FilterCondition]] = Field(
        default=None, description="List of filter conditions"
    )
    group_by: Optional[List[str]] = Field(
        default=None,
        description="Fields to group by (e.g., ['account_type', 'currency'])",
    )
    aggregates: Optional[List[AggregateFunction]] = Field(
        default=None, description="Aggregate functions to apply"
    )
    order_by: Optional[str] = Field(
        default=None, description="Field to order by (e.g., 'total_sum DESC')"
    )
    limit: Optional[int] = Field(
        default=100, ge=1, le=1000, description="Maximum number of groups to return"
    )
    offset: Optional[int] = Field(
        default=0, ge=0, description="Number of groups to skip"
    )


class AggregateResponse(BaseModel):
    """Response model for aggregate queries"""

    groups: List[Dict[str, Any]] = Field(..., description="Grouped results")
    total_groups: int = Field(..., description="Total number of groups")
    limit: Optional[int] = None
    offset: Optional[int] = None
    has_more: bool = Field(..., description="Whether there are more groups")
    filters_applied: List[Dict[str, Any]] = Field(
        default=[], description="Applied filters with localization"
    )
    group_by_fields: List[str] = Field(
        default=[], description="Fields used for grouping"
    )
    aggregate_functions: List[str] = Field(
        default=[], description="Aggregate functions applied"
    )
    query_executed: str = Field(..., description="SQL query executed")
    params_used: List[Any] = Field(default=[], description="Parameters used in query")


class EnhancedAggregateRequest(BaseModel):
    """Enhanced request model for aggregate queries with type filtering and calculated fields"""

    filters: Optional[List[FilterCondition]] = Field(
        default=None, description="List of filter conditions"
    )
    group_by: Optional[List[str]] = Field(
        default=None, description="Fields to group by (e.g., ['month', 'account_type'])"
    )
    aggregates: Optional[List[AggregateFunction]] = Field(
        default=None, description="Aggregate functions to apply"
    )
    order_by: Optional[str] = Field(
        default=None, description="Field to order by (e.g., 'total_sum DESC')"
    )
    limit: Optional[int] = Field(
        default=100, ge=1, le=1000, description="Maximum number of groups to return"
    )
    offset: Optional[int] = Field(
        default=0, ge=0, description="Number of groups to skip"
    )
    account_types: Optional[List[str]] = Field(
        default=None,
        description="Account types to filter by: revenue,cogs,expense,tax,derived",
    )
    calculate_derived: bool = Field(
        default=False, description="Calculate derived metrics like gross profit"
    )
    period_start: Optional[str] = Field(
        default=None, description="Start date (YYYY-MM-DD)"
    )
    period_end: Optional[str] = Field(default=None, description="End date (YYYY-MM-DD)")


class EnhancedAggregateResponse(BaseModel):
    """Enhanced response model for aggregate queries with calculated fields"""

    groups: List[Dict[str, Any]] = Field(
        ..., description="Grouped results with calculated fields"
    )
    total_groups: int = Field(..., description="Total number of groups")
    limit: Optional[int] = None
    offset: Optional[int] = None
    has_more: bool = Field(..., description="Whether there are more groups")
    filters_applied: List[Dict[str, Any]] = Field(
        default=[], description="Applied filters with localization"
    )
    group_by_fields: List[str] = Field(
        default=[], description="Fields used for grouping"
    )
    aggregate_functions: List[str] = Field(
        default=[], description="Aggregate functions applied"
    )
    account_type_filter: Optional[List[str]] = Field(
        default=None, description="Account types filtered"
    )
    calculated_fields: Optional[Dict[str, Any]] = Field(
        default=None, description="Calculated fields like gross profit"
    )
    period_filter: Optional[Dict[str, str]] = Field(
        default=None, description="Period filter applied"
    )
    query_executed: str = Field(..., description="SQL query executed")
    params_used: List[Any] = Field(default=[], description="Parameters used in query")


class SyncResponse(BaseModel):
    """Response model for data sync"""

    success: bool
    message: str
    accounts_created: int
    transactions_created: int
    total_metrics: int


# Period Query Models
class PeriodQueryRequest(BaseModel):
    """Request model for period-based queries"""

    report_type: int = Field(
        ..., description="Report type (1=PL_REPORT, 2=ROOTFI_REPORT)"
    )
    start_date: Optional[str] = Field(
        default=None, description="Start date filter (YYYY-MM-DD)"
    )
    end_date: Optional[str] = Field(
        default=None, description="End date filter (YYYY-MM-DD)"
    )
    account_types: Optional[List[str]] = Field(
        default=None, description="Account types to filter by"
    )
    limit: Optional[int] = Field(
        default=100, ge=1, le=1000, description="Maximum number of records to return"
    )
    offset: Optional[int] = Field(
        default=0, ge=0, description="Number of records to skip"
    )


class PeriodQueryResponse(BaseModel):
    """Response model for period-based queries"""

    data: List[TransactionResponse]
    total_count: int
    report_type: int
    period_filter: Optional[Dict[str, str]] = None
    account_type_filter: Optional[List[str]] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    has_more: bool
    query_summary: Dict[str, Any]


# Legacy Query Models (keeping for backward compatibility)
@dataclass
class QueryRequest:
    """Request model for natural language queries"""

    query: str
    context: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {"query": self.query, "context": self.context}


@dataclass
class QueryResponse:
    """Response model for natural language queries"""

    query: str
    answer: str
    confidence: float = 0.0
    data_points: Optional[List] = None
    insights: Optional[List] = None
    timestamp: Optional[str] = None
    reasoning: Optional[str] = None
    chat_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "query": self.query,
            "answer": self.answer,
            "confidence": self.confidence,
            "data_points": self.data_points,
            "insights": self.insights,
            "timestamp": self.timestamp,
            "reasoning": self.reasoning,
            "chat_id": self.chat_id,
        }
