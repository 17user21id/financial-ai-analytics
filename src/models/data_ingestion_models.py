from dataclasses import dataclass
from typing import Optional, Dict, Any, List


@dataclass
class DataIngestionRequest:
    """Request model for data ingestion"""

    source: str  # "quickbooks" or "rootfi"
    data: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {"source": self.source, "data": self.data}


@dataclass
class DataIngestionResponse:
    """Response model for data ingestion"""

    success: bool
    message: str
    metrics_processed: int
    errors: Optional[List] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "success": self.success,
            "message": self.message,
            "metrics_processed": self.metrics_processed,
            "errors": self.errors,
        }
