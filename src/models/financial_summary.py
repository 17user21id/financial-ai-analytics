from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class FinancialSummary:
    """Financial summary for a period"""

    period_start: str
    period_end: str
    total_revenue: float
    total_expenses: float
    net_profit: float
    operating_profit: float
    profit_margin: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "period_start": self.period_start,
            "period_end": self.period_end,
            "total_revenue": self.total_revenue,
            "total_expenses": self.total_expenses,
            "net_profit": self.net_profit,
            "operating_profit": self.operating_profit,
            "profit_margin": self.profit_margin,
        }
