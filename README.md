# AI-Powered Financial Data Processing System

An intelligent financial data processing system that demonstrates expertise in AI/ML integration, backend architecture, and API design. This system integrates diverse financial data sources into a unified backend and enriches it with powerful AI capabilities for natural language querying and advanced analytics.

## 🚀 Features

### Core Capabilities
- **Data Integration**: Parse and process financial data from multiple sources (JSON formats)
- **AI-Powered Querying**: Natural language interface for financial data analysis
- **Context-Aware Conversations**: Maintains conversation history and context across queries
- **Advanced Analytics**: AI-driven insights including trend analysis, anomaly detection, and health scoring
- **RESTful API**: Clean, well-documented API endpoints for all operations

### AI Features
- **Natural Language Querying**: Ask questions like "What was the total profit in Q1?" or "Show me revenue trends for 2024"
- **Internal Tool Calling Architecture**: Sophisticated orchestration of specialized AI components
- **Intelligent Context Management**: Advanced conversation continuity with semantic analysis
- **Financial Analytics**: Comprehensive analysis, trend detection, anomaly identification, and health scoring

## 🏗️ Architecture

### System Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   FastAPI App   │    │   AI Services   │
│                 │    │                 │    │                 │
│ • JSON Files    │───▶│ • Data Service  │───▶│ • Query Service │
│ • Excel Files   │    │ • AI Service    │    │ • Analytics     │
│ • Database      │    │ • Health Service│    │ • LLM Integration│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   SQLite DB     │
                       │                 │
                       │ • Transactions  │
                       │ • Accounts      │
                       │ • Chat History  │
                       └─────────────────┘
```

## 🧠 AI Architecture

### Internal Tool Calling Architecture
The system implements a sophisticated internal tool calling architecture that orchestrates multiple specialized components with enterprise-grade security and intelligent context management.

```
User Query → Context Retrieval → Internal Tool Chain → Database Interaction → Response Generation
     │              │                    │                      │                      │
     │              │                    │                      │                      │
     ▼              ▼                    ▼                      ▼                      ▼
┌─────────┐   ┌─────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Natural │   │ Intelligent │  │ Internal Tool   │  │ Secure Database │  │ Professional    │
│Language │   │ Context     │  │ Orchestration   │  │ Interaction     │  │ Response        │
│ Query   │   │ Management  │  │ Engine          │  │ Layer           │  │ Generation      │
└─────────┘   └─────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Intelligent Context Management
Advanced context management system that maintains conversation continuity through intelligent summarization and contextual relevance scoring.

```
┌─────────────────────────────────────────────────────────────────┐
│                Intelligent Context Management Layer             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Chat Session  │  │   Context       │  │   Relevance     │ │
│  │   Persistence   │  │   Summarization │  │   Scoring       │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Context Intelligence Engine                  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Historical    │  │   Semantic      │  │   Temporal      │ │
│  │   Context       │  │   Analysis      │  │   Relevance     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Context Flow Example
```
User: "What was the total profit in Q1?"
AI: "Q1 profit was $750,000..."

User: "What about Q2?"  ← Context Resolution
AI: "Q2 profit was $850,000, showing 13% growth from Q1..."
```

### Enterprise Security Features
- **Query Sanitization**: Advanced SQL injection prevention with pattern recognition
- **Parameter Validation**: Strict type checking and range validation
- **Schema Enforcement**: Database schema validation and constraint enforcement
- **Read-Only Enforcement**: Prevents any data modification operations
- **Context Encryption**: Sensitive context data encryption at rest

### Service Architecture
- **Data Service**: Handles data operations (sync, list, aggregate, grouped-metrics, periods, metrics)
- **AI Service**: Processes natural language queries with intelligent context management
- **AI Analytics Service**: Provides advanced financial analytics and insights
- **Health Service**: System health monitoring and status checks

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI
- **Database**: SQLite (with SQLAlchemy ORM)
- **AI/ML**: Azure OpenAI (GPT models)
- **Data Processing**: Pandas, OpenPyXL
- **API Documentation**: FastAPI automatic docs
- **Logging**: Structured logging with multiple levels
- **Configuration**: Environment-based configuration management

## 📋 Prerequisites

- Python 3.11+
- Azure OpenAI API access
- Git

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
git clone <repository-url>
cd AI
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup
```bash
git clone <repository-url>
cd AI
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration (Manual Setup Only)
Create a `.env` file in the root directory:
```bash
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
LLM_MODEL=your_deployment_name
LLM_TEMPERATURE=0.4

# Database Configuration
DATABASE_PATH=financial_data.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=DEV
```

### 4. Azure OpenAI Configuration
```bash
# Copy the example configuration file
cp resources/key_store.json.example resources/key_store.json

# Edit key_store.json with your actual Azure OpenAI credentials
# Replace placeholder values with your actual API key, endpoint, and deployment name
```

### 5. Database Initialization
```bash
# Initialize database with sample data
python -m src.handler.data_sync_handler
```

### 6. Start the Application
```bash
# Development mode
python -m src.api.main

# Or using uvicorn directly
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 7. Access the API
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/health/

## 📊 Data Sources

The system processes financial data from two main sources:

1. **Dataset 1**: Revenue and expense data with account categorization
2. **Dataset 2**: Additional financial metrics and transaction details

Both datasets are automatically parsed and integrated into the unified database schema.

## 🤖 AI Capabilities

### Natural Language Querying
Ask questions in plain English:
- "What was the total revenue last quarter?"
- "Show me the top 5 expense categories"
- "Compare Q1 and Q2 performance"
- "What are the revenue trends for 2024?"

### Context Management
The system maintains conversation context:
- Remembers previous queries and results
- Handles follow-up questions with "above", "that", "same" references
- Provides intelligent context summarization

### Advanced Analytics
- **Comprehensive Analysis**: Complete financial overview with insights
- **Trend Analysis**: Identify patterns and growth trends
- **Anomaly Detection**: Spot unusual financial patterns
- **Health Scoring**: Assess overall financial health

## 🔧 Configuration

### Environment Variables
- `ENVIRONMENT`: TEST/DEV/PROD (affects database and logging settings)
- `DATABASE_PATH`: Path to SQLite database file
- `API_HOST`: API server host (default: 0.0.0.0)
- `API_PORT`: API server port (default: 8000)
- `AZURE_OPENAI_API_KEY`: Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint URL
- `LLM_MODEL`: Azure OpenAI deployment name
- `LLM_TEMPERATURE`: LLM temperature setting (default: 0.4)

### Azure OpenAI Setup
1. Create an Azure OpenAI resource in Azure Portal
2. Deploy a GPT-4 model (recommended: GPT-4 or GPT-4o)
3. Copy `resources/key_store.json.example` to `resources/key_store.json`
4. Update `key_store.json` with your actual Azure OpenAI credentials

**Example key_store.json structure:**
```json
[
  {
    "type": "default",
    "status": "active",
    "details": {
      "openai_api_type": "azure",
      "openai_api_key": "your-actual-api-key",
      "azure_openai_endpoint": "https://your-resource.openai.azure.com",
      "openai_api_version": "2024-02-01",
      "deployment_name": "your-deployment-name",
      "model_name": "your-model-name",
      "temperature": 0.4,
      "request_timeout": 200,
      "max_retries": 2,
      "max_tokens": 4000
    }
  }
]
```

**⚠️ Security Note:** Never commit `key_store.json` to version control. Use `key_store.json.example` as a template.

### Database Configuration
- **TEST**: In-memory SQLite database
- **DEV**: File-based SQLite database with debug logging
- **PROD**: File-based SQLite database with production settings

## 📚 API Usage Examples

### Basic Data Operations
```bash
# Sync data
curl -X POST "http://localhost:8000/api/data/sync"

# Get transaction summary
curl -X GET "http://localhost:8000/api/data/summary"

# Search transactions
curl -X POST "http://localhost:8000/api/data/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "revenue", "limit": 10}'
```

### AI Query Examples
```bash
# Natural language query
curl -X POST "http://localhost:8000/api/ai/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What was the total profit in Q1?",
    "chat_id": "demo_chat",
    "user_id": "demo_user"
  }'

# Follow-up query with context
curl -X POST "http://localhost:8000/api/ai/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What about Q2?",
    "chat_id": "demo_chat",
    "user_id": "demo_user"
  }'
```

### Analytics Examples
```bash
# Comprehensive analysis
curl -X GET "http://localhost:8000/api/ai/analytics/comprehensive"

# Trend analysis
curl -X GET "http://localhost:8000/api/ai/analytics/trends?period_start=2024-01-01&period_end=2024-12-31"

# Anomaly detection
curl -X GET "http://localhost:8000/api/ai/analytics/anomalies"

# Financial health score
curl -X GET "http://localhost:8000/api/ai/analytics/health-score"
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python -m pytest test/

# Run specific test file
python -m pytest test/test_context_refactored.py

# Run with verbose output
python -m pytest test/ -v
```

### Test Coverage
The system includes comprehensive tests for:
- Data integration and parsing
- AI query processing
- Context management
- Database operations
- API endpoints

## 📁 Project Structure

```
AI/
├── src/
│   ├── api/                    # FastAPI application and services
│   │   ├── main.py            # Main FastAPI app
│   │   └── services/          # API service modules
│   ├── config/                 # Configuration management
│   ├── handler/               # Business logic handlers
│   │   ├── ai/                # AI-specific handlers
│   │   ├── financial_handler.py
│   │   └── data_sync_handler.py
│   ├── models/                 # Pydantic models
│   ├── stores/                 # Database stores and managers
│   ├── parsers/                # Data parsing modules
│   └── common/                 # Shared utilities
├── test/                       # Test files
├── resources/                  # Sample data files
├── logs/                       # Application logs
├── requirements.txt           # Python dependencies
├── start.sh                    # Startup script
├── stop.sh                     # Shutdown script
└── README.md                   # This file
```

## 🚀 Deployment

### Local Development
```bash
# Start in development mode
./start.sh

# Stop the application
./stop.sh
```

### Production Deployment
```bash
# Set production environment
export ENVIRONMENT=PROD
export DATABASE_PATH=/var/lib/financial_data.db

# Start production server
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```


## 🔍 Monitoring and Logging

### Log Files
- `logs/app_*.log`: Application logs
- `logs/api_*.log`: API request logs
- `logs/ai_*.log`: AI service logs
- `logs/database_*.log`: Database operation logs
- `logs/error_*.log`: Error logs
- `logs/performance_*.log`: Performance metrics

### Health Monitoring
```bash
# Check system health
curl -X GET "http://localhost:8000/api/health/"
```
