"""
Configuration management for the Financial Data Processing System
Handles environment-based configuration and settings
"""

import os
from enum import Enum
from typing import Optional
from dataclasses import dataclass


class Environment(Enum):
    """Environment types"""

    TEST = "TEST"
    DEV = "DEV"
    PROD = "PROD"


@dataclass
class DatabaseConfig:
    """Database configuration"""

    type: str  # "memory" or "file"
    path: Optional[str] = None
    echo: bool = False


@dataclass
class APIConfig:
    """API configuration"""

    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    reload: bool = False


@dataclass
class AppConfig:
    """Application configuration"""

    environment: Environment
    database: DatabaseConfig
    api: APIConfig
    log_level: str = "INFO"


class ConfigManager:
    """Manages application configuration based on environment"""

    def __init__(self):
        self._config = self._load_config()

    def _load_config(self) -> AppConfig:
        """Load configuration based on environment variables"""
        # Check both ENVIRONMENT and DEV_ENVIRONMENT for backward compatibility
        env_str = os.getenv("ENVIRONMENT", os.getenv("DEV_ENVIRONMENT", "DEV")).upper()

        try:
            environment = Environment(env_str)
        except ValueError:
            print(f"Warning: Invalid environment '{env_str}', defaulting to DEV")
            environment = Environment.DEV

        # Database configuration based on environment
        if environment == Environment.TEST:
            database_config = DatabaseConfig(type="memory", echo=True)
            api_config = APIConfig(host="127.0.0.1", port=8001, debug=True, reload=True)
            log_level = "DEBUG"

        elif environment == Environment.DEV:
            database_config = DatabaseConfig(
                type="file",
                path=os.getenv("DATABASE_PATH", "financial_data.db"),
                echo=True,
            )
            api_config = APIConfig(
                host="0.0.0.0",
                port=int(os.getenv("API_PORT", "8000")),
                debug=True,
                reload=True,
            )
            log_level = "INFO"

        else:  # PROD
            database_config = DatabaseConfig(
                type="file",
                path=os.getenv("DATABASE_PATH", "/var/lib/financial_data.db"),
                echo=False,
            )
            api_config = APIConfig(
                host=os.getenv("API_HOST", "0.0.0.0"),
                port=int(os.getenv("API_PORT", "8000")),
                debug=False,
                reload=False,
            )
            log_level = "WARNING"

        return AppConfig(
            environment=environment,
            database=database_config,
            api=api_config,
            log_level=log_level,
        )

    @property
    def config(self) -> AppConfig:
        """Get current configuration"""
        return self._config

    def is_test_environment(self) -> bool:
        """Check if running in test environment"""
        return self._config.environment == Environment.TEST

    def is_dev_environment(self) -> bool:
        """Check if running in development environment"""
        return self._config.environment == Environment.DEV

    def is_prod_environment(self) -> bool:
        """Check if running in production environment"""
        return self._config.environment == Environment.PROD

    def get_database_url(self) -> str:
        """Get database URL based on configuration"""
        if self._config.database.type == "memory":
            return "sqlite:///:memory:"
        else:
            return f"sqlite:///{self._config.database.path}"

    def print_config(self):
        """Print current configuration (for debugging)"""
        print(f"Environment: {self._config.environment.value}")
        print(f"Database Type: {self._config.database.type}")
        if self._config.database.path:
            print(f"Database Path: {self._config.database.path}")
        print(f"API Host: {self._config.api.host}")
        print(f"API Port: {self._config.api.port}")
        print(f"Debug Mode: {self._config.api.debug}")
        print(f"Log Level: {self._config.log_level}")


# Global configuration instance
config_manager = ConfigManager()
config = config_manager.config
