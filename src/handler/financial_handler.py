"""
Service layer for business logic
"""

import logging
from typing import List, Dict, Any, Optional
from ..stores.database_manager import (
    get_database_manager,
    FilterOperator,
    FilterCondition,
)
from ..config.settings import config_manager

logger = logging.getLogger(__name__)


class FinancialDataHandler:
    """Service class for financial data operations"""

    def __init__(self):
        self.db = get_database_manager()
        self.config = config_manager.config

    def get_metrics_by_type(self, account_type: str, limit: int = 100) -> List[Dict]:
        """Get metrics by account type"""
        return self.db.get_metrics_by_type(account_type, limit)

    def get_metrics_by_period(self, start_date: str, end_date: str) -> List[Dict]:
        """Get all metrics for a specific period"""
        return self.db.get_metrics_by_period(start_date, end_date)

    def get_enhanced_financial_summary(
        self,
        period_start: str,
        period_end: str,
        group_by: str = "none",
        account_type_filter: Optional[List[int]] = None,
        calculate_derived: bool = False,
    ) -> Dict[str, Any]:
        """
        Get enhanced financial summary with grouping, filtering, and derived calculations

        Args:
            period_start: Start date (YYYY-MM-DD)
            period_end: End date (YYYY-MM-DD)
            group_by: Group by period (month, quarter, year) or account_type
            account_type_filter: List of account type IDs to filter by
            calculate_derived: Whether to calculate derived metrics like gross profit

        Returns:
            Enhanced financial summary with grouping and derived metrics
        """
        try:
            logger.info(
                f"Getting enhanced financial summary for {period_start} to {period_end}"
            )
            logger.info(
                f"Group by: {group_by}, Account types: {account_type_filter}, Derived: {calculate_derived}"
            )

            # Get base data
            base_data = self.db.get_metrics_by_period(period_start, period_end)

            # Apply account type filter if specified
            if account_type_filter:
                base_data = [
                    item
                    for item in base_data
                    if item.get("account_type") in account_type_filter
                ]

            # Group data based on group_by parameter
            grouped_data = self._group_financial_data(base_data, group_by)

            # Calculate derived metrics if requested
            if calculate_derived:
                grouped_data = self._calculate_derived_metrics(grouped_data)

            # Create summary response
            summary = {
                "period_start": period_start,
                "period_end": period_end,
                "group_by": group_by,
                "account_type_filter": account_type_filter,
                "calculate_derived": calculate_derived,
                "total_records": len(base_data),
                "grouped_data": grouped_data,
                "summary_stats": self._calculate_summary_stats(grouped_data),
            }

            return summary

        except Exception as e:
            logger.error(f"Error in enhanced financial summary: {e}")
            raise

    def _group_financial_data(self, data: List[Dict], group_by: str) -> Dict[str, Any]:
        """Group financial data by specified criteria"""
        if group_by == "none":
            return {"all": data}

        grouped = {}

        for item in data:
            if group_by == "month":
                # Group by month (YYYY-MM)
                period_start = item.get("period_start", "")
                month_key = period_start[:7] if len(period_start) >= 7 else "unknown"

            elif group_by == "quarter":
                # Group by quarter (YYYY-Q1, Q2, Q3, Q4)
                period_start = item.get("period_start", "")
                if len(period_start) >= 7:
                    year = period_start[:4]
                    month = int(period_start[5:7])
                    quarter = f"Q{(month-1)//3 + 1}"
                    quarter_key = f"{year}-{quarter}"
                else:
                    quarter_key = "unknown"

            elif group_by == "year":
                # Group by year (YYYY)
                period_start = item.get("period_start", "")
                year_key = period_start[:4] if len(period_start) >= 4 else "unknown"

            elif group_by == "account_type":
                # Group by account type
                account_type = item.get("account_type", 0)
                type_names = {
                    1: "revenue",
                    2: "cogs",
                    3: "expense",
                    4: "tax",
                    5: "derived",
                }
                type_key = type_names.get(account_type, f"type_{account_type}")

            else:
                # Default grouping
                type_key = "other"

            # Determine the key to use
            if group_by in ["month", "quarter", "year"]:
                key = locals().get(f"{group_by}_key", "unknown")
            elif group_by == "account_type":
                key = type_key
            else:
                key = "other"

            if key not in grouped:
                grouped[key] = []
            grouped[key].append(item)

        return grouped

    def _calculate_derived_metrics(
        self, grouped_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate derived metrics like gross profit for each group"""
        enhanced_groups = {}

        for group_key, items in grouped_data.items():
            # Calculate totals by account type
            totals = {
                1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 0,
            }  # revenue, cogs, expense, tax, derived

            for item in items:
                account_type = item.get("account_type", 0)
                value = float(item.get("value", 0))
                totals[account_type] += value

            # Calculate derived metrics
            derived_metrics = {
                "gross_profit": totals[1] - totals[2],  # revenue - cogs
                "operating_profit": totals[1]
                - totals[2]
                - totals[3],  # revenue - cogs - expenses
                "net_profit": totals[1]
                - totals[2]
                - totals[3]
                - totals[4],  # revenue - cogs - expenses - tax
                "gross_margin": (
                    (totals[1] - totals[2]) / totals[1] * 100 if totals[1] > 0 else 0
                ),
                "operating_margin": (
                    (totals[1] - totals[2] - totals[3]) / totals[1] * 100
                    if totals[1] > 0
                    else 0
                ),
                "net_margin": (
                    (totals[1] - totals[2] - totals[3] - totals[4]) / totals[1] * 100
                    if totals[1] > 0
                    else 0
                ),
            }

            enhanced_groups[group_key] = {
                "items": items,
                "totals_by_type": totals,
                "derived_metrics": derived_metrics,
            }

        return enhanced_groups

    def _calculate_summary_stats(self, grouped_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate summary statistics across all groups"""
        total_revenue = 0
        total_cogs = 0
        total_expenses = 0
        total_tax = 0
        total_records = 0

        for group_key, group_data in grouped_data.items():
            if isinstance(group_data, dict) and "totals_by_type" in group_data:
                # Enhanced data with derived metrics
                totals = group_data["totals_by_type"]
                total_revenue += totals[1]
                total_cogs += totals[2]
                total_expenses += totals[3]
                total_tax += totals[4]
                total_records += len(group_data["items"])
            else:
                # Simple grouped data
                for item in group_data:
                    account_type = item.get("account_type", 0)
                    value = float(item.get("value", 0))
                    if account_type == 1:
                        total_revenue += value
                    elif account_type == 2:
                        total_cogs += value
                    elif account_type == 3:
                        total_expenses += value
                    elif account_type == 4:
                        total_tax += value
                    total_records += 1

        return {
            "total_revenue": total_revenue,
            "total_cogs": total_cogs,
            "total_expenses": total_expenses,
            "total_tax": total_tax,
            "total_gross_profit": total_revenue - total_cogs,
            "total_operating_profit": total_revenue - total_cogs - total_expenses,
            "total_net_profit": total_revenue - total_cogs - total_expenses - total_tax,
            "total_records": total_records,
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
        }

    def get_available_periods(self) -> List[Dict]:
        """Get all available time periods"""
        return self.db.get_available_periods()

    def get_grouped_metrics(
        self,
        group_by: str,
        filters: List[Dict[str, Any]] = None,
        aggregation: str = "SUM",
        limit: int = 100,
    ) -> List[Dict]:
        """
        Get grouped/aggregated financial metrics with filters

        Args:
            group_by: Field to group by (account_name, account_type, parent_account_id, period_start, period_end)
            filters: List of filter conditions
            aggregation: Aggregation function (SUM, AVG, COUNT, MIN, MAX)
            limit: Maximum number of results

        Returns:
            List of grouped metrics
        """
        try:
            logger.info(
                f"Getting grouped metrics by {group_by} with {len(filters) if filters else 0} filters"
            )

            # Convert filter dictionaries to FilterCondition objects
            filter_conditions = []
            if filters:
                for filter_dict in filters:
                    field = filter_dict.get("field")
                    operator_str = filter_dict.get("operator")
                    value = filter_dict.get("value")
                    value_list = filter_dict.get(
                        "value_list"
                    )  # For IN/NOT_IN operators

                    if field and operator_str:
                        try:
                            operator = FilterOperator(operator_str)

                            # Handle IN and NOT_IN operators with value_list
                            if operator in [FilterOperator.IN, FilterOperator.NOT_IN]:
                                if value_list and isinstance(value_list, list):
                                    filter_condition = FilterCondition(
                                        field, operator, value_list
                                    )
                                else:
                                    logger.warning(
                                        f"IN/NOT_IN operator requires value_list, skipping filter: {field}"
                                    )
                                    continue
                            else:
                                filter_condition = FilterCondition(
                                    field, operator, value
                                )

                            filter_conditions.append(filter_condition)
                        except ValueError:
                            logger.warning(f"Invalid filter operator: {operator_str}")
                            continue

            # Validate group_by field
            valid_group_fields = [
                "account_name",
                "account_type",
                "parent_account_id",
                "period_start",
                "period_end",
            ]
            if group_by not in valid_group_fields:
                raise ValueError(
                    f"Invalid group_by field. Must be one of: {valid_group_fields}"
                )

            # Validate aggregation function
            valid_aggregations = ["SUM", "AVG", "COUNT", "MIN", "MAX"]
            if aggregation.upper() not in valid_aggregations:
                raise ValueError(
                    f"Invalid aggregation. Must be one of: {valid_aggregations}"
                )

            # Use the database's get_metrics_summary method
            results = self.db.get_metrics_summary(group_by, filter_conditions)

            # Apply aggregation to the results
            aggregated_results = []
            for result in results[:limit]:
                aggregated_results.append(
                    {
                        "group_value": result.get(group_by),
                        "aggregation_type": aggregation.upper(),
                        "aggregated_value": result.get("total_value", 0),
                        "record_count": result.get("record_count", 0),
                        "group_by_field": group_by,
                    }
                )

            logger.info(f"Retrieved {len(aggregated_results)} grouped metrics")
            return aggregated_results

        except Exception as e:
            logger.error(f"Error getting grouped metrics: {e}")
            raise
