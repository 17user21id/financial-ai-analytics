"""
Advanced AI Analytics Service
Implements financial trend analysis, anomaly detection, and health scoring
"""

import logging
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass

from .real_llm_service import FinancialLLMService
from .llm_templates import (
    TREND_ANALYSIS_PROMPT,
    ANOMALY_DETECTION_PROMPT,
    FINANCIAL_HEALTH_PROMPT,
)
from .enum_mappings import EnumMappings
from ...stores.database_manager import FilterOperator, FilterCondition
from ...handler.financial_handler import FinancialDataHandler
from ...common.enums import AccountType

logger = logging.getLogger(__name__)


@dataclass
class TrendAnalysis:
    """Trend analysis result"""

    trend_type: str
    direction: str  # "increasing", "decreasing", "stable"
    percentage_change: float
    confidence: float
    insights: List[str]
    recommendations: List[str]


@dataclass
class AnomalyDetection:
    """Anomaly detection result"""

    anomaly_type: str
    severity: str  # "low", "medium", "high"
    description: str
    affected_accounts: List[str]
    suggested_actions: List[str]
    confidence: float


@dataclass
class FinancialHealthScore:
    """Financial health score result"""

    overall_score: float  # 0-100
    component_scores: Dict[str, float]
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    risk_level: str  # "low", "medium", "high"


class AnalyticsDataFormatter:
    """Shared data formatting utilities for analytics"""

    @staticmethod
    def _get_account_type_name(account_type: int) -> str:
        """Convert account type enum to readable string"""
        try:
            return AccountType(account_type).name.replace("_", " ").title()
        except (ValueError, AttributeError):
            return f"Unknown Type {account_type}"

    @staticmethod
    def format_financial_summary(data: List[Dict]) -> str:
        """Format financial data for analysis"""
        # Group by account type
        by_type = {}
        for item in data:
            account_type = item["account_type"]
            if account_type not in by_type:
                by_type[account_type] = []
            by_type[account_type].append(item)

        formatted_parts = []
        formatted_parts.append("Financial Data Summary:")
        formatted_parts.append("=" * 50)

        for account_type, items in by_type.items():
            total_value = sum(item["value"] for item in items)
            avg_value = total_value / len(items) if items else 0

            formatted_parts.append(
                f"\n{AnalyticsDataFormatter._get_account_type_name(account_type)}:"
            )
            formatted_parts.append(f"  Total Value: ${total_value:,.2f}")
            formatted_parts.append(f"  Number of Records: {len(items)}")
            formatted_parts.append(f"  Average Value: ${avg_value:,.2f}")

            # Show top 3 accounts by value
            top_accounts = sorted(items, key=lambda x: x["value"], reverse=True)[:3]
            formatted_parts.append("  Top Accounts:")
            for account in top_accounts:
                formatted_parts.append(
                    f"    - {account['account_name']}: ${account['value']:,.2f}"
                )

        return "\n".join(formatted_parts)

    @staticmethod
    def format_anomaly_data(data: List[Dict]) -> str:
        """Format data specifically for anomaly detection"""
        formatted_parts = []
        formatted_parts.append("Financial Data for Anomaly Detection:")
        formatted_parts.append("=" * 50)

        # Sort by value to identify outliers
        sorted_data = sorted(data, key=lambda x: x["value"], reverse=True)

        formatted_parts.append(f"\nTop 10 Highest Values:")
        for i, item in enumerate(sorted_data[:10]):
            formatted_parts.append(
                f"{i+1}. {item['account_name']}: ${item['value']:,.2f} ({item['account_type']})"
            )

        formatted_parts.append(f"\nBottom 10 Lowest Values:")
        for i, item in enumerate(sorted_data[-10:]):
            formatted_parts.append(
                f"{i+1}. {item['account_name']}: ${item['value']:,.2f} ({item['account_type']})"
            )

        # Statistical summary
        values = [item["value"] for item in data]
        if values:
            avg_value = sum(values) / len(values)
            max_value = max(values)
            min_value = min(values)

            formatted_parts.append(f"\nStatistical Summary:")
            formatted_parts.append(f"Average Value: ${avg_value:,.2f}")
            formatted_parts.append(f"Maximum Value: ${max_value:,.2f}")
            formatted_parts.append(f"Minimum Value: ${min_value:,.2f}")
            formatted_parts.append(f"Value Range: ${max_value - min_value:,.2f}")

        return "\n".join(formatted_parts)

    @staticmethod
    def format_health_data(data: List[Dict]) -> str:
        """Format data specifically for health scoring"""
        formatted_parts = []
        formatted_parts.append("Financial Data for Health Scoring:")
        formatted_parts.append("=" * 50)

        # Calculate key metrics
        revenue_data = [d for d in data if d["account_type"] == "revenue"]
        expense_data = [d for d in data if d["account_type"] == "operating_expense"]
        profit_data = [d for d in data if "profit" in d["account_name"].lower()]

        total_revenue = sum(d["value"] for d in revenue_data)
        total_expenses = sum(d["value"] for d in expense_data)
        total_profit = sum(d["value"] for d in profit_data)

        formatted_parts.append(f"\nKey Financial Metrics:")
        formatted_parts.append(f"Total Revenue: ${total_revenue:,.2f}")
        formatted_parts.append(f"Total Operating Expenses: ${total_expenses:,.2f}")
        formatted_parts.append(f"Total Profit: ${total_profit:,.2f}")

        if total_revenue > 0:
            profit_margin = (total_profit / total_revenue) * 100
            expense_ratio = (total_expenses / total_revenue) * 100
            formatted_parts.append(f"Profit Margin: {profit_margin:.2f}%")
            formatted_parts.append(f"Expense Ratio: {expense_ratio:.2f}%")

        # Account distribution
        account_types = {}
        for item in data:
            account_type = item["account_type"]
            account_types[account_type] = account_types.get(account_type, 0) + 1

        formatted_parts.append(f"\nAccount Distribution:")
        for account_type, count in account_types.items():
            formatted_parts.append(
                f"{AnalyticsDataFormatter._get_account_type_name(account_type)}: {count} accounts"
            )

        return "\n".join(formatted_parts)

    @staticmethod
    def format_enum_mappings(enum_mappings: dict) -> str:
        """Format enum mappings for AI context"""
        formatted_parts = []

        for enum_name, enum_data in enum_mappings.items():
            formatted_parts.append(f"{enum_name}:")
            formatted_parts.append(f"  Description: {enum_data['description']}")
            formatted_parts.append("  Values:")

            for value in enum_data["values"]:
                formatted_parts.append(
                    f"    - {value['name']} ({value['value']}): {value['description']}"
                )

            if "examples" in enum_data:
                formatted_parts.append("  Examples:")
                for example in enum_data["examples"]:
                    formatted_parts.append(f"    {example}")

            formatted_parts.append("")  # Empty line between enums

        return "\n".join(formatted_parts)


class FinancialTrendAnalyzer:
    """Analyzes financial trends using AI"""

    def __init__(self, llm_service):
        self.llm_service = llm_service
        logger.info("Financial Trend Analyzer initialized")

    def analyze_trends(self, data: List[Dict]) -> TrendAnalysis:
        """Analyze financial trends using AI"""
        logger.info(f"Analyzing trends for {len(data)} data points")

        try:
            # Format data for analysis
            formatted_data = AnalyticsDataFormatter.format_financial_summary(data)

            # Get enum mappings for context
            enum_mappings = EnumMappings.get_all_enum_definitions()
            enum_mappings_str = AnalyticsDataFormatter.format_enum_mappings(
                enum_mappings
            )

            prompt = f"{TREND_ANALYSIS_PROMPT.format(enum_mappings=enum_mappings_str)}\n\n{formatted_data}"

            # Use Azure OpenAI for trend analysis
            response = self.llm_service.get_financial_analysis(
                query=prompt, financial_data=formatted_data
            )

            # Parse response and create trend analysis
            trend_analysis = self._parse_trend_response(response.answer, data)

            logger.info(
                f"Trend analysis completed with confidence: {trend_analysis.confidence}"
            )
            return trend_analysis

        except Exception as e:
            logger.error(f"Error in trend analysis: {e}")
            return self._create_default_trend_analysis()

    def _parse_trend_response(self, response: str, data: List[Dict]) -> TrendAnalysis:
        """Parse Azure OpenAI response into structured trend analysis"""
        try:
            # Calculate actual metrics from data
            revenue_data = [d for d in data if d["account_type"] == "revenue"]
            expense_data = [d for d in data if d["account_type"] == "operating_expense"]

            total_revenue = sum(d["value"] for d in revenue_data)
            total_expenses = sum(d["value"] for d in expense_data)

            # Determine trend direction
            if total_revenue > total_expenses:
                direction = "increasing"
                percentage_change = (
                    ((total_revenue - total_expenses) / total_expenses * 100)
                    if total_expenses > 0
                    else 0
                )
            else:
                direction = "decreasing"
                percentage_change = (
                    ((total_expenses - total_revenue) / total_revenue * 100)
                    if total_revenue > 0
                    else 0
                )

            # Extract insights from Azure OpenAI response
            insights = self._extract_insights_from_response(response)
            recommendations = self._extract_recommendations_from_response(response)

            # If no insights extracted, use basic data insights
            if not insights:
                insights = [
                    f"Revenue totals ${total_revenue:,.2f} across {len(revenue_data)} accounts",
                    f"Operating expenses total ${total_expenses:,.2f} across {len(expense_data)} accounts",
                    f"Net position shows {direction} trend with {abs(percentage_change):.1f}% difference",
                ]

            if not recommendations:
                recommendations = [
                    "Monitor revenue growth patterns for sustainability",
                    "Review expense categories for optimization opportunities",
                    "Implement regular financial health checks",
                ]

            return TrendAnalysis(
                trend_type="comprehensive_analysis",
                direction=direction,
                percentage_change=round(percentage_change, 2),
                confidence=0.9,  # High confidence for Azure OpenAI
                insights=insights,
                recommendations=recommendations,
            )

        except Exception as e:
            logger.error(f"Error parsing trend response: {e}")
            return self._create_default_trend_analysis()

    def _extract_insights_from_response(self, response: str) -> List[str]:
        """Extract insights from Azure OpenAI response"""
        insights = []
        lines = response.split("\n")

        for line in lines:
            line = line.strip()
            # Look for insights (bullet points, numbered lists, or key phrases)
            if (
                line.startswith(("•", "-", "*", "1.", "2.", "3.", "4.", "5."))
                or "insight" in line.lower()
                or "finding" in line.lower()
                or "analysis" in line.lower()
            ):
                if len(line) > 10:  # Avoid very short lines
                    insights.append(line)

        # If no structured insights found, extract key sentences
        if not insights:
            sentences = response.split(".")
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 20 and any(
                    keyword in sentence.lower()
                    for keyword in [
                        "revenue",
                        "expense",
                        "profit",
                        "trend",
                        "growth",
                        "decline",
                        "increase",
                        "decrease",
                    ]
                ):
                    insights.append(sentence + ".")
                    if len(insights) >= 3:  # Limit to top 3 insights
                        break

        return insights[:5]  # Return max 5 insights

    def _extract_recommendations_from_response(self, response: str) -> List[str]:
        """Extract recommendations from Azure OpenAI response"""
        recommendations = []
        lines = response.split("\n")

        for line in lines:
            line = line.strip()
            # Look for recommendations (bullet points, numbered lists, or key phrases)
            if (
                line.startswith(("•", "-", "*", "1.", "2.", "3.", "4.", "5."))
                or "recommend" in line.lower()
                or "suggest" in line.lower()
                or "action" in line.lower()
            ):
                if len(line) > 10:  # Avoid very short lines
                    recommendations.append(line)

        # If no structured recommendations found, extract key sentences
        if not recommendations:
            sentences = response.split(".")
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 20 and any(
                    keyword in sentence.lower()
                    for keyword in [
                        "recommend",
                        "suggest",
                        "should",
                        "action",
                        "improve",
                        "optimize",
                        "focus",
                    ]
                ):
                    recommendations.append(sentence + ".")
                    if len(recommendations) >= 3:  # Limit to top 3 recommendations
                        break

        return recommendations[:5]  # Return max 5 recommendations

    def _create_default_trend_analysis(self) -> TrendAnalysis:
        """Create default trend analysis when error occurs"""
        return TrendAnalysis(
            trend_type="general",
            direction="stable",
            percentage_change=0.0,
            confidence=0.5,
            insights=["Unable to analyze trends due to data processing error"],
            recommendations=["Review data quality and try again"],
        )


class FinancialAnomalyDetector:
    """Detects anomalies in financial data using AI"""

    def __init__(self, llm_service):
        self.llm_service = llm_service
        logger.info("Financial Anomaly Detector initialized")

    def detect_anomalies(self, data: List[Dict]) -> List[AnomalyDetection]:
        """Detect anomalies in financial data using AI"""
        logger.info(f"Detecting anomalies in {len(data)} data points")

        try:
            # Format data for anomaly detection
            formatted_data = AnalyticsDataFormatter.format_anomaly_data(data)

            # Get enum mappings for context
            enum_mappings = EnumMappings.get_all_enum_definitions()
            enum_mappings_str = AnalyticsDataFormatter.format_enum_mappings(
                enum_mappings
            )

            prompt = f"{ANOMALY_DETECTION_PROMPT.format(enum_mappings=enum_mappings_str)}\n\n{formatted_data}"

            # Use Azure OpenAI for anomaly detection
            response = self.llm_service.get_anomaly_detection(formatted_data)

            # Parse response and create anomaly detections
            anomalies = self._parse_anomaly_response(response.answer, data)

            logger.info(
                f"Anomaly detection completed. Found {len(anomalies)} anomalies"
            )
            return anomalies

        except Exception as e:
            logger.error(f"Error in anomaly detection: {e}")
            return [self._create_default_anomaly()]

    def _parse_anomaly_response(
        self, response: str, data: List[Dict]
    ) -> List[AnomalyDetection]:
        """Parse Azure OpenAI response into structured anomaly detections"""
        anomalies = []

        # Calculate statistical anomalies
        values = [item["value"] for item in data if item["value"] != 0]
        if len(values) > 1:
            avg_value = sum(values) / len(values)
            max_value = max(values)

            # Detect high-value outliers
            if max_value > avg_value * 5:  # 5x average threshold
                high_value_items = [
                    item for item in data if item["value"] > avg_value * 5
                ]

                anomalies.append(
                    AnomalyDetection(
                        anomaly_type="high_value_outlier",
                        severity="medium",
                        description=f"Found {len(high_value_items)} accounts with values significantly above average",
                        affected_accounts=[
                            item["account_name"] for item in high_value_items[:3]
                        ],
                        suggested_actions=[
                            "Review high-value transactions for accuracy",
                            "Verify these accounts are correctly categorized",
                            "Investigate if these are one-time or recurring items",
                        ],
                        confidence=0.8,
                    )
                )

        # Detect zero-value accounts
        zero_value_items = [item for item in data if item["value"] == 0]
        if zero_value_items:
            anomalies.append(
                AnomalyDetection(
                    anomaly_type="zero_value_accounts",
                    severity="low",
                    description=f"Found {len(zero_value_items)} accounts with zero values",
                    affected_accounts=[
                        item["account_name"] for item in zero_value_items[:5]
                    ],
                    suggested_actions=[
                        "Verify if zero values are expected",
                        "Check for missing data entry",
                        "Review account setup and configuration",
                    ],
                    confidence=0.7,
                )
            )

        # If no statistical anomalies found, create a general one
        if not anomalies:
            anomalies.append(
                AnomalyDetection(
                    anomaly_type="data_quality_check",
                    severity="low",
                    description="No significant anomalies detected in the data",
                    affected_accounts=[],
                    suggested_actions=[
                        "Continue regular monitoring",
                        "Maintain current data quality standards",
                    ],
                    confidence=0.6,
                )
            )

        return anomalies

    def _create_default_anomaly(self) -> AnomalyDetection:
        """Create default anomaly detection when error occurs"""
        return AnomalyDetection(
            anomaly_type="analysis_error",
            severity="low",
            description="Unable to complete anomaly detection due to processing error",
            affected_accounts=[],
            suggested_actions=["Review data format and try again"],
            confidence=0.3,
        )


class FinancialHealthScorer:
    """Calculates financial health score using AI"""

    def __init__(self, llm_service):
        self.llm_service = llm_service
        logger.info("Financial Health Scorer initialized")

    def calculate_health_score(self, data: List[Dict]) -> FinancialHealthScore:
        """Calculate comprehensive financial health score using AI"""
        logger.info(f"Calculating health score for {len(data)} data points")

        try:
            # Format data for health scoring
            formatted_data = AnalyticsDataFormatter.format_health_data(data)

            # Get enum mappings for context
            enum_mappings = EnumMappings.get_all_enum_definitions()
            enum_mappings_str = AnalyticsDataFormatter.format_enum_mappings(
                enum_mappings
            )

            prompt = f"{FINANCIAL_HEALTH_PROMPT.format(enum_mappings=enum_mappings_str)}\n\n{formatted_data}"

            # Use Azure OpenAI for health scoring
            response = self.llm_service.get_health_score(formatted_data)

            # Parse response and create health score
            health_score = self._parse_health_response(response.answer, data)

            logger.info(f"Health score calculated: {health_score.overall_score}/100")
            return health_score

        except Exception as e:
            logger.error(f"Error in health scoring: {e}")
            return self._create_default_health_score()

    def _parse_health_response(
        self, response: str, data: List[Dict]
    ) -> FinancialHealthScore:
        """Parse Azure OpenAI response into structured health score"""
        try:
            # Extract health score from Azure OpenAI response
            ai_score = self._extract_health_score_from_response(response)

            # Calculate actual metrics as backup
            revenue_data = [d for d in data if d["account_type"] == "revenue"]
            expense_data = [d for d in data if d["account_type"] == "operating_expense"]
            profit_data = [d for d in data if "profit" in d["account_name"].lower()]

            total_revenue = sum(d["value"] for d in revenue_data)
            total_expenses = sum(d["value"] for d in expense_data)
            total_profit = sum(d["value"] for d in profit_data)

            # Use AI score if available, otherwise calculate
            if ai_score:
                overall_score = ai_score["overall_score"]
                component_scores = ai_score["component_scores"]
                strengths = ai_score["strengths"]
                weaknesses = ai_score["weaknesses"]
                recommendations = ai_score["recommendations"]
                risk_level = ai_score["risk_level"]
            else:
                # Calculate component scores
                revenue_score = min(
                    100, max(0, (total_revenue / 1000000) * 20)
                )  # Scale based on revenue
                expense_score = (
                    min(100, max(0, 100 - (total_expenses / total_revenue * 100)))
                    if total_revenue > 0
                    else 50
                )
                profit_score = (
                    min(100, max(0, (total_profit / total_revenue * 100) * 2))
                    if total_revenue > 0
                    else 50
                )

                # Calculate overall score
                overall_score = (revenue_score + expense_score + profit_score) / 3

                component_scores = {
                    "revenue_growth": round(revenue_score, 1),
                    "expense_management": round(expense_score, 1),
                    "profitability": round(profit_score, 1),
                }

                strengths = [
                    f"Strong revenue base of ${total_revenue:,.2f}",
                    (
                        f"Profit margin of {(total_profit/total_revenue*100):.1f}%"
                        if total_revenue > 0
                        else "Positive profit position"
                    ),
                    f"Diverse account structure with {len(data)} financial records",
                ]

                weaknesses = [
                    "Monitor expense growth relative to revenue",
                    "Ensure consistent profit margins",
                    "Regular financial health monitoring recommended",
                ]

                recommendations = [
                    "Implement regular financial health checks",
                    "Monitor key performance indicators",
                    "Review expense categories for optimization",
                    "Maintain strong revenue growth momentum",
                ]

                # Determine risk level
                if overall_score >= 80:
                    risk_level = "low"
                elif overall_score >= 60:
                    risk_level = "medium"
                else:
                    risk_level = "high"

            return FinancialHealthScore(
                overall_score=round(overall_score, 1),
                component_scores=component_scores,
                strengths=strengths,
                weaknesses=weaknesses,
                recommendations=recommendations,
                risk_level=risk_level,
            )

        except Exception as e:
            logger.error(f"Error parsing health response: {e}")
            return self._create_default_health_score()

    def _extract_health_score_from_response(self, response: str) -> Optional[Dict]:
        """Extract health score from Azure OpenAI response"""
        try:
            import re

            # Look for score patterns
            score_patterns = [
                r"overall score[:\s]*(\d+(?:\.\d+)?)",
                r"health score[:\s]*(\d+(?:\.\d+)?)",
                r"score[:\s]*(\d+(?:\.\d+)?)/100",
                r"(\d+(?:\.\d+)?)/100",
            ]

            overall_score = None
            for pattern in score_patterns:
                match = re.search(pattern, response.lower())
                if match:
                    overall_score = float(match.group(1))
                    break

            if not overall_score:
                return None

            # Extract component scores
            component_scores = {}
            component_patterns = {
                "revenue_growth": r"revenue[:\s]*(\d+(?:\.\d+)?)",
                "expense_management": r"expense[:\s]*(\d+(?:\.\d+)?)",
                "profitability": r"profit[:\s]*(\d+(?:\.\d+)?)",
            }

            for component, pattern in component_patterns.items():
                match = re.search(pattern, response.lower())
                if match:
                    component_scores[component] = float(match.group(1))

            # Extract strengths, weaknesses, recommendations
            strengths = self._extract_list_from_response(
                response, ["strength", "positive", "good"]
            )
            weaknesses = self._extract_list_from_response(
                response, ["weakness", "negative", "concern"]
            )
            recommendations = self._extract_list_from_response(
                response, ["recommend", "suggest", "action"]
            )

            # Determine risk level
            risk_level = "medium"
            if overall_score >= 80:
                risk_level = "low"
            elif overall_score < 60:
                risk_level = "high"

            return {
                "overall_score": overall_score,
                "component_scores": component_scores,
                "strengths": strengths,
                "weaknesses": weaknesses,
                "recommendations": recommendations,
                "risk_level": risk_level,
            }

        except Exception as e:
            logger.error(f"Error extracting health score: {e}")
            return None

    def _extract_list_from_response(
        self, response: str, keywords: List[str]
    ) -> List[str]:
        """Extract list items from response based on keywords"""
        items = []
        lines = response.split("\n")

        in_section = False
        for line in lines:
            line = line.strip()

            # Check if we're entering a relevant section
            if any(keyword in line.lower() for keyword in keywords):
                in_section = True
                continue

            # Extract items from the section
            if in_section and (
                line.startswith(("•", "-", "*", "1.", "2.", "3."))
                or any(
                    keyword in line.lower()
                    for keyword in ["strength", "weakness", "recommend"]
                )
            ):
                if len(line) > 10:
                    items.append(line)

            # Stop if we hit another section
            if in_section and any(
                keyword in line.lower()
                for keyword in ["recommendation", "risk", "conclusion"]
            ):
                break

        return items[:5]  # Return max 5 items

    def _create_default_health_score(self) -> FinancialHealthScore:
        """Create default health score when error occurs"""
        return FinancialHealthScore(
            overall_score=50.0,
            component_scores={
                "revenue_growth": 50.0,
                "expense_management": 50.0,
                "profitability": 50.0,
            },
            strengths=["Data processing capabilities available"],
            weaknesses=["Unable to complete full health assessment"],
            recommendations=["Review data quality and retry analysis"],
            risk_level="medium",
        )


class AdvancedAnalyticsService:
    """Main service for advanced AI analytics"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AdvancedAnalyticsService, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        financial_service=None,
        llm_provider: str = "azure",
        llm_model: str = None,
        llm_temperature: float = 0.4,
    ):
        # Only initialize once
        if hasattr(self, "_initialized"):
            return

        self.financial_service = financial_service or FinancialDataHandler()

        # Get singleton instance of LLM service (Azure OpenAI)
        try:
            self.llm_service = FinancialLLMService.get_instance(
                provider="azure", model_name=llm_model, temperature=llm_temperature
            )
            logger.info(f"Using Azure OpenAI LLM service for analytics (singleton)")
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI service: {e}")
            logger.error("   No fallback available - AI analytics will fail.")
            raise RuntimeError(f"Failed to initialize LLM service: {e}")

        self.trend_analyzer = FinancialTrendAnalyzer(self.llm_service)
        self.anomaly_detector = FinancialAnomalyDetector(self.llm_service)
        self.health_scorer = FinancialHealthScorer(self.llm_service)

        self._initialized = True
        logger.info("Advanced Analytics Service initialized (singleton)")

    @classmethod
    def get_instance(
        cls,
        financial_service=None,
        llm_provider: str = "azure",
        llm_model: str = None,
        llm_temperature: float = 0.4,
    ):
        """Get singleton instance of AdvancedAnalyticsService"""
        if cls._instance is None:
            cls._instance = cls(
                financial_service, llm_provider, llm_model, llm_temperature
            )
        return cls._instance

    def get_comprehensive_analysis(
        self, period_start: str = None, period_end: str = None
    ) -> Dict[str, Any]:
        """Get comprehensive financial analysis including trends, anomalies, and health score"""
        logger.info(
            f"Getting comprehensive analysis for period: {period_start} to {period_end}"
        )

        try:
            # Get financial data
            filters = []
            if period_start:
                filters.append(
                    FilterCondition(
                        "period_start", FilterOperator.GREATER_THAN_EQUAL, period_start
                    )
                )
            if period_end:
                filters.append(
                    FilterCondition(
                        "period_end", FilterOperator.LESS_THAN_EQUAL, period_end
                    )
                )

            data = self.financial_service.db.query_metrics(filters=filters, limit=1000)

            if not data:
                return {
                    "error": "No data found for the specified period",
                    "period_start": period_start,
                    "period_end": period_end,
                }

            # Perform all analyses
            trend_analysis = self.trend_analyzer.analyze_trends(data)
            anomalies = self.anomaly_detector.detect_anomalies(data)
            health_score = self.health_scorer.calculate_health_score(data)

            return {
                "analysis_timestamp": datetime.now().isoformat(),
                "period_start": period_start,
                "period_end": period_end,
                "data_points_analyzed": len(data),
                "trend_analysis": {
                    "trend_type": trend_analysis.trend_type,
                    "direction": trend_analysis.direction,
                    "percentage_change": trend_analysis.percentage_change,
                    "confidence": trend_analysis.confidence,
                    "insights": trend_analysis.insights,
                    "recommendations": trend_analysis.recommendations,
                },
                "anomaly_detection": [
                    {
                        "anomaly_type": anomaly.anomaly_type,
                        "severity": anomaly.severity,
                        "description": anomaly.description,
                        "affected_accounts": anomaly.affected_accounts,
                        "suggested_actions": anomaly.suggested_actions,
                        "confidence": anomaly.confidence,
                    }
                    for anomaly in anomalies
                ],
                "financial_health": {
                    "overall_score": health_score.overall_score,
                    "component_scores": health_score.component_scores,
                    "strengths": health_score.strengths,
                    "weaknesses": health_score.weaknesses,
                    "recommendations": health_score.recommendations,
                    "risk_level": health_score.risk_level,
                },
            }

        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {e}")
            return {
                "error": f"Analysis failed: {str(e)}",
                "period_start": period_start,
                "period_end": period_end,
            }

    def get_trend_analysis(
        self, period_start: str = None, period_end: str = None
    ) -> Dict[str, Any]:
        """Get trend analysis only"""
        logger.info("Getting trend analysis")

        try:
            filters = []
            if period_start:
                filters.append(
                    FilterCondition(
                        "period_start", FilterOperator.GREATER_THAN_EQUAL, period_start
                    )
                )
            if period_end:
                filters.append(
                    FilterCondition(
                        "period_end", FilterOperator.LESS_THAN_EQUAL, period_end
                    )
                )

            data = self.financial_service.db.query_metrics(filters=filters, limit=500)
            trend_analysis = self.trend_analyzer.analyze_trends(data)

            return {
                "analysis_timestamp": datetime.now().isoformat(),
                "period_start": period_start,
                "period_end": period_end,
                "data_points_analyzed": len(data),
                "trend_analysis": {
                    "trend_type": trend_analysis.trend_type,
                    "direction": trend_analysis.direction,
                    "percentage_change": trend_analysis.percentage_change,
                    "confidence": trend_analysis.confidence,
                    "insights": trend_analysis.insights,
                    "recommendations": trend_analysis.recommendations,
                },
            }

        except Exception as e:
            logger.error(f"Error in trend analysis: {e}")
            return {"error": f"Trend analysis failed: {str(e)}"}

    def get_anomaly_detection(
        self, period_start: str = None, period_end: str = None
    ) -> Dict[str, Any]:
        """Get anomaly detection only"""
        logger.info("Getting anomaly detection")

        try:
            filters = []
            if period_start:
                filters.append(
                    FilterCondition(
                        "period_start", FilterOperator.GREATER_THAN_EQUAL, period_start
                    )
                )
            if period_end:
                filters.append(
                    FilterCondition(
                        "period_end", FilterOperator.LESS_THAN_EQUAL, period_end
                    )
                )

            data = self.financial_service.db.query_metrics(filters=filters, limit=500)
            anomalies = self.anomaly_detector.detect_anomalies(data)

            return {
                "analysis_timestamp": datetime.now().isoformat(),
                "period_start": period_start,
                "period_end": period_end,
                "data_points_analyzed": len(data),
                "anomalies_found": len(anomalies),
                "anomaly_detection": [
                    {
                        "anomaly_type": anomaly.anomaly_type,
                        "severity": anomaly.severity,
                        "description": anomaly.description,
                        "affected_accounts": anomaly.affected_accounts,
                        "suggested_actions": anomaly.suggested_actions,
                        "confidence": anomaly.confidence,
                    }
                    for anomaly in anomalies
                ],
            }

        except Exception as e:
            logger.error(f"Error in anomaly detection: {e}")
            return {"error": f"Anomaly detection failed: {str(e)}"}

    def get_health_score(
        self, period_start: str = None, period_end: str = None
    ) -> Dict[str, Any]:
        """Get financial health score only"""
        logger.info("Getting financial health score")

        try:
            filters = []
            if period_start:
                filters.append(
                    FilterCondition(
                        "period_start", FilterOperator.GREATER_THAN_EQUAL, period_start
                    )
                )
            if period_end:
                filters.append(
                    FilterCondition(
                        "period_end", FilterOperator.LESS_THAN_EQUAL, period_end
                    )
                )

            data = self.financial_service.db.query_metrics(filters=filters, limit=500)
            health_score = self.health_scorer.calculate_health_score(data)

            return {
                "analysis_timestamp": datetime.now().isoformat(),
                "period_start": period_start,
                "period_end": period_end,
                "data_points_analyzed": len(data),
                "financial_health": {
                    "overall_score": health_score.overall_score,
                    "component_scores": health_score.component_scores,
                    "strengths": health_score.strengths,
                    "weaknesses": health_score.weaknesses,
                    "recommendations": health_score.recommendations,
                    "risk_level": health_score.risk_level,
                },
            }

        except Exception as e:
            logger.error(f"Error in health scoring: {e}")
            return {"error": f"Health scoring failed: {str(e)}"}
