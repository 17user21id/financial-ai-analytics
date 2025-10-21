"""
System Logging System for Financial Data Processing
Creates daily log files with comprehensive logging capabilities
"""

import logging
import logging.handlers
from datetime import datetime, date
from pathlib import Path
from typing import Optional, Dict, Any
import json
import traceback
from functools import wraps
import sys

from .enums import LogComponent


class SystemLogger:
    """System logging system with daily file rotation and structured logging"""

    def __init__(
        self,
        log_dir: str = "logs",
        app_name: str = "financial_ai",
        log_level: str = "INFO",
        max_file_size: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 30,
    ):  # Keep 30 days of logs
        """
        Initialize system logger

        Args:
            log_dir: Directory to store log files
            app_name: Application name for log file naming
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            max_file_size: Maximum size of each log file before rotation
            backup_count: Number of backup files to keep
        """
        self.log_dir = Path(log_dir)
        self.app_name = app_name
        self.log_level = getattr(logging, log_level.upper())
        self.max_file_size = max_file_size
        self.backup_count = backup_count

        # Create logs directory if it doesn't exist
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Initialize loggers dictionary
        self.loggers: Dict[LogComponent, logging.Logger] = {}
        self._setup_loggers()

        # Log system startup
        self.info(
            "System Logger initialized",
            extra={
                "log_dir": str(self.log_dir),
                "app_name": self.app_name,
                "log_level": log_level,
                "max_file_size": self.max_file_size,
                "backup_count": self.backup_count,
            },
        )

    def _setup_loggers(self):
        """Setup different loggers for different components"""
        for component in LogComponent:
            level = logging.ERROR if component == LogComponent.ERROR else None
            self.loggers[component] = self._create_logger(
                name=f"{self.app_name}.{component.value}",
                filename=self._get_log_filename(component.value),
                level=level,
            )

    def _get_log_filename(self, component: str) -> str:
        """Generate log filename with date"""
        today = date.today().strftime("%Y-%m-%d")
        return self.log_dir / f"{component}_{today}.log"

    def _create_logger(
        self, name: str, filename: str, level: Optional[int] = None
    ) -> logging.Logger:
        """Create a logger with file handler and console handler"""
        logger = logging.getLogger(name)
        logger.setLevel(level or self.log_level)

        # Clear existing handlers
        logger.handlers.clear()

        # Create formatters
        detailed_formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        simple_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S"
        )

        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            filename=filename,
            maxBytes=self.max_file_size,
            backupCount=self.backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(detailed_formatter)
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(simple_formatter)
        console_handler.setLevel(logging.INFO)

        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # Prevent propagation to root logger
        logger.propagate = False

        return logger

    def _log_with_context(
        self,
        component: LogComponent,
        level: int,
        message: str,
        extra: Optional[Dict[str, Any]] = None,
        log_to_error: bool = False,
    ):
        """
        Log message with additional context

        Args:
            component: Log component
            level: Log level
            message: Log message
            extra: Additional context data
            log_to_error: Also log to error file
        """
        if extra:
            context_str = json.dumps(extra, default=str)
            full_message = f"{message} | Context: {context_str}"
        else:
            full_message = message

        self.loggers[component].log(level, full_message)

        # Also log to error file for errors
        if log_to_error and component != LogComponent.ERROR:
            error_message = f"{component.value.upper()} Error: {message}"
            self.loggers[LogComponent.ERROR].log(
                level,
                (
                    error_message
                    if not extra
                    else f"{error_message} | Context: {context_str}"
                ),
            )

    # Generic logging methods
    def _log(
        self,
        component: LogComponent,
        level: int,
        message: str,
        extra: Optional[Dict[str, Any]] = None,
        log_to_error: bool = False,
    ):
        """Generic log method"""
        self._log_with_context(component, level, message, extra, log_to_error)

    # Application logging methods
    def info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log info message"""
        self._log(LogComponent.APP, logging.INFO, message, extra)

    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log debug message"""
        self._log(LogComponent.APP, logging.DEBUG, message, extra)

    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log warning message"""
        self._log(LogComponent.APP, logging.WARNING, message, extra)

    def error(
        self,
        message: str,
        extra: Optional[Dict[str, Any]] = None,
        exc_info: bool = True,
    ):
        """Log error message with exception info"""
        if exc_info:
            extra = extra or {}
            extra["exception"] = traceback.format_exc()
        self._log(LogComponent.APP, logging.ERROR, message, extra, log_to_error=True)

    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log critical message"""
        self._log(LogComponent.APP, logging.CRITICAL, message, extra, log_to_error=True)

    # Component-specific logging methods
    def ai_info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log AI service info"""
        self._log(LogComponent.AI, logging.INFO, message, extra)

    def ai_debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log AI service debug"""
        self._log(LogComponent.AI, logging.DEBUG, message, extra)

    def ai_error(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log AI service error"""
        self._log(LogComponent.AI, logging.ERROR, message, extra, log_to_error=True)

    def db_info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log database info"""
        self._log(LogComponent.DATABASE, logging.INFO, message, extra)

    def db_error(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log database error"""
        self._log(
            LogComponent.DATABASE, logging.ERROR, message, extra, log_to_error=True
        )

    def api_info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log API info"""
        self._log(LogComponent.API, logging.INFO, message, extra)

    def api_error(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log API error"""
        self._log(LogComponent.API, logging.ERROR, message, extra, log_to_error=True)

    def parser_info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log parser info"""
        self._log(LogComponent.PARSER, logging.INFO, message, extra)

    def parser_error(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log parser error"""
        self._log(LogComponent.PARSER, logging.ERROR, message, extra, log_to_error=True)

    def perf_info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log performance info"""
        self._log(LogComponent.PERFORMANCE, logging.INFO, message, extra)

    # Specialized logging methods with common pattern
    def _build_log_info(
        self, base_info: Dict[str, Any], extra: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Build log info dictionary with timestamp"""
        base_info["timestamp"] = datetime.now().isoformat()
        if extra:
            base_info.update(extra)
        return base_info

    def log_api_request(
        self,
        method: str,
        endpoint: str,
        status_code: int,
        response_time: float,
        extra: Optional[Dict[str, Any]] = None,
    ):
        """Log API request details"""
        request_info = self._build_log_info(
            {
                "method": method,
                "endpoint": endpoint,
                "status_code": status_code,
                "response_time": response_time,
            },
            extra,
        )

        self.api_info(f"API Request: {method} {endpoint} - {status_code}", request_info)

        if response_time > 5.0:  # Log slow requests
            self.perf_info(
                f"Slow API Request: {method} {endpoint} took {response_time:.3f}s",
                request_info,
            )

    def log_ai_query(
        self,
        query: str,
        response: str,
        confidence: float,
        processing_time: float,
        extra: Optional[Dict[str, Any]] = None,
    ):
        """Log AI query processing"""
        query_info = self._build_log_info(
            {
                "query": query,
                "response_length": len(response),
                "confidence": confidence,
                "processing_time": processing_time,
            },
            extra,
        )

        self.ai_info(f"AI Query processed: {query[:50]}...", query_info)

        if processing_time > 10.0:  # Log slow AI queries
            self.perf_info(f"Slow AI Query: {processing_time:.3f}s", query_info)

    def log_database_operation(
        self,
        operation: str,
        table: str,
        rows_affected: int,
        execution_time: float,
        extra: Optional[Dict[str, Any]] = None,
    ):
        """Log database operations"""
        db_info = self._build_log_info(
            {
                "operation": operation,
                "table": table,
                "rows_affected": rows_affected,
                "execution_time": execution_time,
            },
            extra,
        )

        self.db_info(f"DB Operation: {operation} on {table}", db_info)

        if execution_time > 2.0:  # Log slow DB operations
            self.perf_info(
                f"Slow DB Operation: {operation} took {execution_time:.3f}s", db_info
            )


# Decorator for automatic function logging
def log_function_calls(logger: SystemLogger):
    """Decorator to automatically log function calls and results"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            func_name = func.__name__
            module_name = func.__module__

            try:
                result = func(*args, **kwargs)
                execution_time = (datetime.now() - start_time).total_seconds()

                # Log function result with performance
                logger.debug(
                    f"Function completed: {func_name}",
                    {
                        "function": func_name,
                        "module": module_name,
                        "execution_time": execution_time,
                        "result_type": type(result).__name__,
                    },
                )

                if execution_time > 1.0:  # Log slow functions
                    logger.perf_info(
                        f"Slow function: {func_name} took {execution_time:.3f}s",
                        {
                            "function": func_name,
                            "module": module_name,
                            "execution_time": execution_time,
                        },
                    )

                return result

            except Exception as e:
                execution_time = (datetime.now() - start_time).total_seconds()

                # Log function error
                logger.error(
                    f"Function {func_name} failed",
                    extra={
                        "function": func_name,
                        "module": module_name,
                        "execution_time": execution_time,
                        "error": str(e),
                    },
                )
                raise

        return wrapper

    return decorator


# Global logger instance
system_logger = SystemLogger()


# Convenience functions for easy access
def get_logger() -> SystemLogger:
    """Get the global system logger instance"""
    return system_logger


def log_info(message: str, extra: Optional[Dict[str, Any]] = None):
    """Log info message"""
    system_logger.info(message, extra)


def log_error(message: str, extra: Optional[Dict[str, Any]] = None):
    """Log error message"""
    system_logger.error(message, extra)


def log_ai_query(
    query: str,
    response: str,
    confidence: float,
    processing_time: float,
    extra: Optional[Dict[str, Any]] = None,
):
    """Log AI query"""
    system_logger.log_ai_query(query, response, confidence, processing_time, extra)


def log_api_request(
    method: str,
    endpoint: str,
    status_code: int,
    response_time: float,
    extra: Optional[Dict[str, Any]] = None,
):
    """Log API request"""
    system_logger.log_api_request(method, endpoint, status_code, response_time, extra)
