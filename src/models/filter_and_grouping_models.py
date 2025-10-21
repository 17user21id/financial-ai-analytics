from dataclasses import dataclass
from typing import Optional, Any, List, Dict


@dataclass
class FilterRequest:
    """Request model for filter conditions"""

    field: str
    operator: str
    value: Any = None
    value_list: Optional[List[Any]] = None


@dataclass
class GroupedMetricsRequest:
    """Request model for grouped metrics query"""

    group_by: str
    filters: Optional[List[FilterRequest]] = None
    aggregation: str = "SUM"
    limit: int = 100


@dataclass
class GroupedMetricsResponse:
    """Response model for grouped metrics"""

    group_value: Any
    aggregation_type: str
    aggregated_value: float
    record_count: int
    group_by_field: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "group_value": self.group_value,
            "aggregation_type": self.aggregation_type,
            "aggregated_value": self.aggregated_value,
            "record_count": self.record_count,
            "group_by_field": self.group_by_field,
        }
