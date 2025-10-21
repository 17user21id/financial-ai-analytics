"""Azure OpenAI LLM Service for Financial Data Processing"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from abc import ABC, abstractmethod

try:
    from langchain_openai import AzureChatOpenAI

    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False
    raise ImportError(
        "Azure OpenAI libraries not installed. Run: pip install langchain-openai"
    )

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """LLM response with confidence and metadata"""

    answer: str
    confidence: float
    reasoning: Optional[str] = None
    model_used: Optional[str] = None
    tokens_used: Optional[int] = None


class KeyStore:
    """Manages Azure OpenAI credentials from resources/key_store.json"""

    def __init__(self, key_file: str = "resources/key_store.json"):
        self.key_file = key_file
        self.keys = self._load_keys()
        logger.info(f"KeyStore initialized with {len(self.keys)} keys")

    def _load_keys(self) -> Dict:
        try:
            if os.path.exists(self.key_file):
                with open(self.key_file, "r") as f:
                    return json.load(f)
            else:
                logger.warning(f"KeyStore file {self.key_file} not found")
                return {}
        except Exception as e:
            logger.error(f"Error loading KeyStore: {e}")
            return {}

    def get_active_key_details(self, key_type: str) -> tuple[bool, Dict]:
        # Handle both list format and old keys format for backward compatibility
        keys_list = (
            self.keys if isinstance(self.keys, list) else self.keys.get("keys", [])
        )
        for key in keys_list:
            if key.get("type") == key_type and key.get("status") == "active":
                return True, key.get("details", {})
        return False, {}

    def add_key(self, key_type: str, details: Dict, status: str = "active"):
        # Handle both list format and old keys format for backward compatibility
        if isinstance(self.keys, list):
            keys_list = self.keys
        else:
            if "keys" not in self.keys:
                self.keys["keys"] = []
            keys_list = self.keys["keys"]

        new_key = {
            "type": key_type,
            "status": status,
            "details": details,
            "created_at": datetime.now().isoformat(),
        }

        keys_list.append(new_key)
        self._save_keys()
        logger.info(f"Added key: {key_type}")

    def _save_keys(self):
        try:
            with open(self.key_file, "w") as f:
                json.dump(self.keys, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving KeyStore: {e}")


class BaseLLMService(ABC):
    """Base class for LLM services"""

    def __init__(self, model_name: str = None, temperature: float = None):
        self.model_name = model_name
        self.temperature = temperature
        self.keystore = KeyStore()

    @abstractmethod
    def get_response(self, prompt: str, context: str = "") -> LLMResponse:
        pass

    def _calculate_confidence(self, logprobs: List[float] = None) -> float:
        """Calculate confidence from logprobs"""
        if not logprobs:
            return 0.8

        try:
            probs = [2**lp for lp in logprobs if lp is not None]
            if probs:
                geometric_mean = (1.0 / len(probs)) * sum(probs)
                return min(0.95, max(0.1, geometric_mean))
        except Exception as e:
            logger.warning(f"Error calculating confidence: {e}")

        return 0.8


class AzureOpenAIService(BaseLLMService):
    """Azure OpenAI service"""

    def __init__(self, model_name: str = None, temperature: float = None):
        super().__init__(model_name, temperature)
        self.llm = None
        self._initialize_model()

    def _initialize_model(self):
        try:
            # Get default configuration from key store
            found, credentials = self.keystore.get_active_key_details("default")

            if not found:
                raise ValueError("Default Azure credentials not found in key store")

            # Set environment variables from configuration
            os.environ["OPENAI_API_TYPE"] = credentials.get("openai_api_type")
            os.environ["AZURE_OPENAI_API_KEY"] = credentials.get("openai_api_key")
            os.environ["AZURE_OPENAI_ENDPOINT"] = credentials.get(
                "azure_openai_endpoint"
            )
            os.environ["OPENAI_API_VERSION"] = credentials.get("openai_api_version")

            # Validate required configuration values
            required_fields = [
                "openai_api_type",
                "openai_api_key",
                "azure_openai_endpoint",
                "openai_api_version",
                "deployment_name",
            ]

            missing_fields = [
                field for field in required_fields if not credentials.get(field)
            ]
            if missing_fields:
                raise ValueError(
                    f"Missing required configuration fields: {missing_fields}"
                )

            # Get configuration values from key store
            deployment_name = credentials.get("deployment_name")
            model_name = credentials.get("model_name")
            temperature = credentials.get("temperature")
            request_timeout = credentials.get("request_timeout")
            max_retries = credentials.get("max_retries")
            max_tokens = credentials.get("max_tokens")

            if not deployment_name:
                raise ValueError("deployment_name not found in configuration")

            # Update instance variables with configuration values
            self.model_name = model_name or deployment_name
            self.temperature = temperature

            self.llm = AzureChatOpenAI(
                deployment_name=deployment_name,
                temperature=self.temperature,
                request_timeout=request_timeout,
                max_retries=max_retries,
                max_tokens=max_tokens,
            )

            logger.info(
                f"Azure OpenAI initialized: {self.model_name} (deployment: {deployment_name})"
            )

        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI: {e}")
            raise

    def get_response(self, prompt: str, context: str = "") -> LLMResponse:
        try:
            if not self.llm:
                raise ValueError("Azure OpenAI model not initialized")

            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            response = self.llm.invoke(full_prompt)
            answer = response.content
            logprobs = getattr(response, "logprobs", None)
            confidence = self._calculate_confidence(logprobs)

            return LLMResponse(
                answer=answer,
                confidence=confidence,
                reasoning=f"Generated by Azure OpenAI {self.model_name}",
                model_used=self.model_name,
                tokens_used=getattr(response, "usage", {}).get("total_tokens", 0),
            )

        except Exception as e:
            logger.error(f"Error getting Azure OpenAI response: {e}")
            return LLMResponse(
                answer=f"I encountered an error processing your request: {str(e)}",
                confidence=0.0,
                reasoning=f"Error from Azure OpenAI: {str(e)}",
                model_used=self.model_name,
            )


class LLMServiceFactory:
    """Factory for creating Azure OpenAI service"""

    @staticmethod
    def create_service(
        provider: str = "azure", model_name: str = None, temperature: float = None
    ) -> BaseLLMService:
        if provider.upper() != "AZURE":
            logger.warning(f"Provider '{provider}' not supported. Using Azure OpenAI.")

        if not AZURE_AVAILABLE:
            raise ImportError(
                "Azure OpenAI libraries not installed. Run: pip install langchain-openai"
            )

        return AzureOpenAIService(model_name, temperature)


class FinancialLLMService:
    """Singleton Azure OpenAI service for financial analysis"""

    _instance = None
    _initialized = False

    def __new__(
        cls, provider: str = "azure", model_name: str = None, temperature: float = None
    ):
        if cls._instance is None:
            cls._instance = super(FinancialLLMService, cls).__new__(cls)
        return cls._instance

    def __init__(
        self, provider: str = "azure", model_name: str = None, temperature: float = None
    ):
        if self._initialized:
            logger.debug("LLM Service already initialized")
            return

        self.provider = "azure"
        self.model_name = model_name
        self.temperature = temperature

        try:
            self.llm_service = LLMServiceFactory.create_service(
                provider="azure",
                model_name=self.model_name,
                temperature=self.temperature,
            )
            logger.info(f"Financial LLM Service initialized")
            FinancialLLMService._initialized = True

        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI: {e}")
            raise

    @classmethod
    def get_instance(
        cls, provider: str = "azure", model_name: str = None, temperature: float = None
    ):
        """Get singleton instance"""
        if cls._instance is None:
            cls._instance = FinancialLLMService(provider, model_name, temperature)
        return cls._instance

    @classmethod
    def reset_instance(cls):
        """Reset singleton (for testing)"""
        cls._instance = None
        cls._initialized = False
        logger.info("LLM Service reset")

    def get_response(self, prompt: str, context: str = "") -> LLMResponse:
        return self.llm_service.get_response(prompt, context)

    def get_financial_analysis(self, query: str, financial_data: str) -> LLMResponse:
        context = f"""You are a senior financial analyst. Analyze the following financial data and provide insights.
        
Financial Data: {financial_data}

Guidelines: Provide specific numbers, insights, trends, key findings. Use professional language. Be concise."""
        return self.get_response(query, context)

    def get_trend_analysis(self, financial_data: str) -> LLMResponse:
        prompt = """Analyze financial data for trends: revenue patterns, expense management, profitability, 
        business implications, and strategic recommendations."""
        return self.get_financial_analysis(prompt, financial_data)

    def get_anomaly_detection(self, financial_data: str) -> LLMResponse:
        prompt = """Detect anomalies: unusual spikes/drops, inconsistent patterns, outliers, unexpected changes.
        For each: type, severity, description, affected accounts, investigation actions."""
        return self.get_financial_analysis(prompt, financial_data)

    def get_health_score(self, financial_data: str) -> LLMResponse:
        prompt = """Calculate financial health score (0-100). Evaluate: revenue growth, profitability, 
        expense control, cash flow, stability. Provide: overall score, component scores, strengths, 
        weaknesses, recommendations, risk level."""
        return self.get_financial_analysis(prompt, financial_data)
