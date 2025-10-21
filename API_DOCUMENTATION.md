# API Documentation

This document provides comprehensive API documentation for the AI-Powered Financial Data Processing System, including all endpoints with detailed examples and curl commands.

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API does not require authentication. All endpoints are publicly accessible.

## Response Format
All API responses follow a consistent JSON format:
```json
{
  "status": "success|error",
  "data": {...},
  "message": "Optional message",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

---

## 📊 Data Service Endpoints

### 1. Sync Data
Synchronizes and processes financial data from source files.

**Endpoint:** `POST /api/data/sync`

**Description:** Processes Excel data files and imports them into the database.

**Request Body:** None

**Response:**
```json
{
  "status": "success",
  "data": {
    "processed_files": 2,
    "transactions_imported": 150,
    "accounts_created": 25,
    "processing_time": "2.5s"
  },
  "message": "Data synchronization completed successfully"
}
```

**Curl Example:**
```bash
curl -X POST "http://localhost:8000/api/data/sync" \
  -H "Content-Type: application/json"
```

---

### 2. List Transactions
Retrieves a paginated list of financial transactions.

**Endpoint:** `POST /api/data/list`

**Description:** Returns transactions with optional filtering and pagination.

**Request Body:**
```json
{
  "filters": [
    {
      "field": "account_type",
      "operator": "=",
      "value": "revenue"
    },
    {
      "field": "period_start",
      "operator": ">=",
      "value": "2024-01-01"
    }
  ],
  "order_by": "period_start",
  "limit": 20,
  "offset": 0
}
```

**Response:**
```json
{
  "data": [
    {
      "tx_id": 1,
      "account_id": 5,
      "value": 50000.00,
      "period_start": "2024-01-01",
      "period_end": "2024-01-31",
      "source_id": 1,
      "account_name": "Sales Revenue",
      "account_type": "Revenue",
      "account_sub_type": "Operating Revenue",
      "currency": "USD",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total_count": 150,
  "limit": 20,
  "offset": 0
}
```

**Curl Example:**
```bash
curl -X POST "http://localhost:8000/api/data/list" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": [
      {
        "field": "account_type",
        "operator": "=",
        "value": "revenue"
      }
    ],
    "order_by": "period_start",
    "limit": 20,
    "offset": 0
  }'
```

---

### 3. Get Transaction by ID
Retrieves a specific transaction by its ID.

**Endpoint:** `GET /api/data/list/{tx_id}`

**Description:** Returns detailed information for a specific transaction.

**Path Parameters:**
- `tx_id` (required): Transaction ID

**Query Parameters:**
- `language` (optional): Language code for localization (default: "en")

**Response:**
```json
{
  "tx_id": 1,
  "account_id": 5,
  "value": 50000.00,
  "period_start": "2024-01-01",
  "period_end": "2024-01-31",
  "source_id": 1,
  "account_name": "Sales Revenue",
  "account_type": "Revenue",
  "account_sub_type": "Operating Revenue",
  "currency": "USD",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Curl Example:**
```bash
curl -X GET "http://localhost:8000/api/data/list/1?language=en"
```

---

### 4. Enhanced Aggregate Data
Performs enhanced aggregations on financial data with calculated fields.

**Endpoint:** `POST /api/data/aggregate`

**Description:** Executes enhanced aggregation queries with grouping, filtering, and calculated derived metrics.

**Request Body:**
```json
{
  "group_by": ["account_type", "month"],
  "aggregates": [
    {
      "function": "SUM",
      "field": "value",
      "alias": "total_value"
    },
    {
      "function": "COUNT",
      "field": "*",
      "alias": "transaction_count"
    }
  ],
  "filters": [
    {
      "field": "account_type",
      "operator": "IN",
      "value": [1, 2, 3]
    }
  ],
  "account_types": ["revenue", "cogs", "expense"],
  "period_start": "2024-01-01",
  "period_end": "2024-12-31",
  "calculate_derived": true,
  "order_by": "total_value",
  "limit": 50,
  "offset": 0
}
```

**Response:**
```json
{
  "groups": [
    {
      "account_type": 1,
      "month": "2024-01",
      "total_value": 750000.00,
      "transaction_count": 30
    }
  ],
  "total_count": 1,
  "account_type_filter": ["revenue", "cogs", "expense"],
  "calculated_fields": {
    "gross_profit": 500000.00,
    "operating_profit": 300000.00,
    "net_profit": 250000.00,
    "gross_margin_percent": 66.67,
    "operating_margin_percent": 40.0,
    "net_margin_percent": 33.33,
    "total_revenue": 750000.00,
    "total_cogs": 250000.00,
    "total_expenses": 200000.00,
    "total_tax": 50000.00
  },
  "period_filter": {
    "start": "2024-01-01",
    "end": "2024-12-31"
  }
}
```

**Curl Example:**
```bash
curl -X POST "http://localhost:8000/api/data/aggregate" \
  -H "Content-Type: application/json" \
  -d '{
    "group_by": ["account_type", "month"],
    "aggregates": [
      {
        "function": "SUM",
        "field": "value",
        "alias": "total_value"
      }
    ],
    "account_types": ["revenue", "cogs", "expense"],
    "period_start": "2024-01-01",
    "period_end": "2024-12-31",
    "calculate_derived": true,
    "limit": 50
  }'
```

---

### 5. Grouped Metrics
Retrieves grouped financial metrics with custom filtering.

**Endpoint:** `POST /api/data/grouped-metrics`

**Description:** Returns grouped financial metrics with advanced filtering capabilities.

**Request Body:**
```json
{
  "group_by": "account_type",
  "filters": [
    {
      "field": "period_start",
      "operator": ">=",
      "value": "2024-01-01"
    },
    {
      "field": "period_end",
      "operator": "<=",
      "value": "2024-12-31"
    }
  ],
  "aggregation": "SUM",
  "limit": 100
}
```

**Response:**
```json
[
  {
    "group_value": "Revenue",
    "aggregation_type": "SUM",
    "aggregated_value": 2500000.00,
    "record_count": 150,
    "group_by_field": "account_type"
  },
  {
    "group_value": "Expense",
    "aggregation_type": "SUM",
    "aggregated_value": 1800000.00,
    "record_count": 120,
    "group_by_field": "account_type"
  }
]
```

**Curl Example:**
```bash
curl -X POST "http://localhost:8000/api/data/grouped-metrics" \
  -H "Content-Type: application/json" \
  -d '{
    "group_by": "account_type",
    "filters": [
      {
        "field": "period_start",
        "operator": ">=",
        "value": "2024-01-01"
      }
    ],
    "aggregation": "SUM",
    "limit": 100
  }'
```

---

### 6. Get Available Periods
Retrieves available time periods in the dataset.

**Endpoint:** `GET /api/data/periods`

**Description:** Returns all available time periods for filtering.

**Response:**
```json
{
  "periods": [
    "2024-01-01",
    "2024-02-01",
    "2024-03-01",
    "2024-04-01",
    "2024-05-01",
    "2024-06-01"
  ],
  "count": 6
}
```

**Curl Example:**
```bash
curl -X GET "http://localhost:8000/api/data/periods"
```

---

### 7. Get Metrics by Account Type
Retrieves financial metrics filtered by account type.

**Endpoint:** `GET /api/data/metrics/{account_type}`

**Description:** Returns financial metrics for a specific account type.

**Path Parameters:**
- `account_type` (required): Account type (revenue, cogs, operating_expense, non_operating_revenue, non_operating_expense, tax, derived)

**Query Parameters:**
- `limit` (optional): Maximum number of results (default: 100)

**Response:**
```json
{
  "account_type": "revenue",
  "count": 25,
  "data": [
    {
      "account_id": 1,
      "account_name": "Sales Revenue",
      "total_value": 1500000.00,
      "transaction_count": 50,
      "avg_value": 30000.00
    }
  ]
}
```

**Curl Example:**
```bash
curl -X GET "http://localhost:8000/api/data/metrics/revenue?limit=50"
```

---

## 🤖 AI Service Endpoints

### 1. Process AI Query
Processes natural language queries using AI.

**Endpoint:** `POST /api/ai/query`

**Description:** Converts natural language questions into SQL queries and returns formatted responses.

**Request Body:**
```json
{
  "query": "What was the total profit in Q1?",
  "chat_id": "demo_chat_001",
  "user_id": "demo_user",
  "use_v2": true
}
```

**Query Parameters:**
- `use_v2` (optional): Use internal tool calling architecture (default: true)

**Response:**
```json
{
  "query": "What was the total profit in Q1?",
  "answer": "The total profit for Q1 2024 was $750,000. This represents a 15% increase compared to the previous quarter. The profit margin was 25%, indicating strong operational efficiency.",
  "confidence": 0.95,
  "data_points": [
    {
      "metric": "Total Profit",
      "value": 750000.00,
      "period": "Q1 2024",
      "change_percent": 15.0
    }
  ],
  "insights": [
    "Profit increased by 15% quarter-over-quarter",
    "Operating margin improved to 25%",
    "Revenue growth outpaced expense growth"
  ],
  "timestamp": "2024-01-15T10:30:00Z",
  "chat_id": "demo_chat_001"
}
```

**Curl Example:**
```bash
curl -X POST "http://localhost:8000/api/ai/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What was the total profit in Q1?",
    "chat_id": "demo_chat_001",
    "user_id": "demo_user",
    "use_v2": true
  }'
```

**Follow-up Query Example:**
```bash
curl -X POST "http://localhost:8000/api/ai/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What about Q2?",
    "chat_id": "demo_chat_001",
    "user_id": "demo_user"
  }'
```

---

## 📈 AI Analytics Service Endpoints

### 1. Comprehensive Analysis
Performs comprehensive AI-powered financial analysis.

**Endpoint:** `GET /api/ai/analytics/comprehensive`

**Description:** Provides detailed financial analysis with AI-generated insights.

**Query Parameters:**
- `period_start` (optional): Start date in YYYY-MM-DD format
- `period_end` (optional): End date in YYYY-MM-DD format

**Response:**
```json
{
  "status": "success",
  "data": {
    "analysis_type": "comprehensive",
    "period": {
      "start": "2024-01-01",
      "end": "2024-12-31"
    },
    "financial_metrics": {
      "total_revenue": 2500000.00,
      "total_expenses": 1800000.00,
      "gross_profit": 700000.00,
      "operating_margin": 28.0,
      "net_profit": 650000.00
    },
    "ai_insights": [
      "Revenue growth shows consistent upward trend with 15% YoY increase",
      "Operating expenses are well-controlled at 72% of revenue",
      "Profit margins indicate healthy business operations",
      "Cash flow patterns suggest seasonal business model"
    ],
    "recommendations": [
      "Consider expanding high-margin product lines",
      "Monitor expense growth to maintain profitability",
      "Implement cash flow forecasting for seasonal planning"
    ],
    "risk_factors": [
      "Concentration risk in top revenue accounts",
      "Seasonal dependency may impact cash flow"
    ],
    "generated_at": "2024-01-15T10:30:00Z"
  }
}
```

**Curl Example:**
```bash
curl -X GET "http://localhost:8000/api/ai/analytics/comprehensive?period_start=2024-01-01&period_end=2024-12-31"
```

---

### 2. Trend Analysis
Identifies financial trends and patterns.

**Endpoint:** `GET /api/ai/analytics/trends`

**Description:** Analyzes financial trends over time with AI-powered pattern recognition.

**Query Parameters:**
- `period_start` (optional): Start date in YYYY-MM-DD format
- `period_end` (optional): End date in YYYY-MM-DD format

**Response:**
```json
{
  "status": "success",
  "data": {
    "analysis_type": "trend_analysis",
    "period": {
      "start": "2024-01-01",
      "end": "2024-12-31"
    },
    "trends": [
      {
        "metric": "Revenue",
        "trend_direction": "increasing",
        "trend_strength": "strong",
        "growth_rate": 15.2,
        "pattern": "linear_growth",
        "description": "Revenue shows consistent linear growth with 15.2% annual increase"
      },
      {
        "metric": "Operating Expenses",
        "trend_direction": "increasing",
        "trend_strength": "moderate",
        "growth_rate": 8.5,
        "pattern": "seasonal",
        "description": "Operating expenses show seasonal patterns with moderate 8.5% growth"
      }
    ],
    "seasonal_patterns": [
      {
        "metric": "Revenue",
        "peak_month": "December",
        "low_month": "February",
        "seasonality_strength": 0.75,
        "description": "Strong seasonal pattern with December peak and February low"
      }
    ],
    "forecast": {
      "next_quarter_revenue": 675000.00,
      "confidence_interval": 0.85,
      "forecast_method": "seasonal_arima"
    },
    "generated_at": "2024-01-15T10:30:00Z"
  }
}
```

**Curl Example:**
```bash
curl -X GET "http://localhost:8000/api/ai/analytics/trends?period_start=2024-01-01&period_end=2024-12-31"
```

---

### 3. Anomaly Detection
Identifies unusual patterns and anomalies in financial data.

**Endpoint:** `GET /api/ai/analytics/anomalies`

**Description:** Detects anomalies and unusual patterns in financial data.

**Query Parameters:**
- `period_start` (optional): Start date in YYYY-MM-DD format
- `period_end` (optional): End date in YYYY-MM-DD format
- `sensitivity` (optional): Anomaly detection sensitivity (low, medium, high)

**Response:**
```json
{
  "status": "success",
  "data": {
    "analysis_type": "anomaly_detection",
    "period": {
      "start": "2024-01-01",
      "end": "2024-12-31"
    },
    "anomalies": [
      {
        "anomaly_id": "ANOM_001",
        "type": "spike",
        "severity": "high",
        "metric": "Revenue",
        "date": "2024-06-15",
        "expected_value": 45000.00,
        "actual_value": 125000.00,
        "deviation_percent": 177.8,
        "description": "Unusual revenue spike detected in June, 177.8% above expected value",
        "possible_causes": [
          "Large one-time sale",
          "Seasonal event",
          "Data entry error"
        ]
      },
      {
        "anomaly_id": "ANOM_002",
        "type": "drop",
        "severity": "medium",
        "metric": "Operating Expenses",
        "date": "2024-09-01",
        "expected_value": 150000.00,
        "actual_value": 75000.00,
        "deviation_percent": -50.0,
        "description": "Significant expense drop in September, 50% below expected",
        "possible_causes": [
          "Cost reduction initiative",
          "Delayed expense recognition",
          "Accounting adjustment"
        ]
      }
    ],
    "summary": {
      "total_anomalies": 2,
      "high_severity": 1,
      "medium_severity": 1,
      "low_severity": 0,
      "detection_confidence": 0.92
    },
    "generated_at": "2024-01-15T10:30:00Z"
  }
}
```

**Curl Example:**
```bash
curl -X GET "http://localhost:8000/api/ai/analytics/anomalies?period_start=2024-01-01&period_end=2024-12-31&sensitivity=medium"
```

---

### 4. Financial Health Score
Calculates AI-powered financial health score.

**Endpoint:** `GET /api/ai/analytics/health-score`

**Description:** Provides comprehensive financial health assessment with scoring.

**Query Parameters:**
- `period_start` (optional): Start date in YYYY-MM-DD format
- `period_end` (optional): End date in YYYY-MM-DD format

**Response:**
```json
{
  "status": "success",
  "data": {
    "analysis_type": "financial_health_score",
    "period": {
      "start": "2024-01-01",
      "end": "2024-12-31"
    },
    "overall_score": {
      "score": 78,
      "grade": "B+",
      "rating": "Good",
      "description": "Strong financial health with room for improvement in liquidity management"
    },
    "score_breakdown": {
      "profitability": {
        "score": 85,
        "weight": 0.3,
        "description": "Strong profitability with healthy margins"
      },
      "liquidity": {
        "score": 65,
        "weight": 0.25,
        "description": "Adequate liquidity but could be improved"
      },
      "efficiency": {
        "score": 80,
        "weight": 0.2,
        "description": "Good operational efficiency"
      },
      "growth": {
        "score": 82,
        "weight": 0.15,
        "description": "Strong growth trajectory"
      },
      "stability": {
        "score": 75,
        "weight": 0.1,
        "description": "Moderate stability with some volatility"
      }
    },
    "key_metrics": {
      "profit_margin": 28.0,
      "revenue_growth": 15.2,
      "expense_ratio": 72.0,
      "cash_flow_coverage": 1.2
    },
    "recommendations": [
      "Improve cash flow management to enhance liquidity score",
      "Maintain current profitability levels",
      "Consider diversifying revenue streams for stability",
      "Implement expense monitoring systems"
    ],
    "risk_assessment": {
      "overall_risk": "Low-Medium",
      "primary_risks": [
        "Seasonal cash flow variability",
        "Concentration in key revenue sources"
      ],
      "mitigation_strategies": [
        "Establish cash reserves for seasonal periods",
        "Diversify customer base and revenue streams"
      ]
    },
    "generated_at": "2024-01-15T10:30:00Z"
  }
}
```

**Curl Example:**
```bash
curl -X GET "http://localhost:8000/api/ai/analytics/health-score?period_start=2024-01-01&period_end=2024-12-31"
```

---

## 🏥 Health Service Endpoints

### 1. Health Check
Performs system health check.

**Endpoint:** `GET /api/health/`

**Description:** Returns system status and health information.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "environment": "DEV",
  "database_type": "file"
}
```

**Curl Example:**
```bash
curl -X GET "http://localhost:8000/api/health/"
```

---

### 2. Basic Health Check
Performs basic health check with minimal information.

**Endpoint:** `GET /api/health/basic`

**Description:** Returns basic health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "message": "Service is running"
}
```

**Curl Example:**
```bash
curl -X GET "http://localhost:8000/api/health/basic"
```

---

## 🔄 Legacy Endpoints

### 1. Legacy Query Endpoint
Legacy endpoint for backward compatibility.

**Endpoint:** `POST /query`

**Description:** Legacy endpoint that redirects to the new AI service.

**Request Body:**
```json
{
  "query": "What was the total revenue?"
}
```

**Response:**
```json
{
  "query": "What was the total revenue?",
  "answer": "The total revenue is $2,500,000.00 across all periods.",
  "confidence": 0.95,
  "data_points": [
    {
      "metric": "Total Revenue",
      "value": 2500000.00
    }
  ],
  "insights": [
    "Revenue shows strong performance across all periods",
    "Consistent growth pattern observed"
  ],
  "timestamp": "2024-01-15T10:30:00Z",
  "note": "This is a legacy endpoint. Use /api/ai/query for the new API."
}
```

**Curl Example:**
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What was the total revenue?"
  }'
```

---

## 📋 Root Endpoint

### 1. API Information
Returns API information and available services.

**Endpoint:** `GET /`

**Description:** Provides API overview and service information.

**Response:**
```json
{
  "message": "Financial Data Processing System",
  "version": "1.0.0",
  "environment": "DEV",
  "database_type": "file",
  "architecture": "Organized service architecture with multiple specialized services",
  "services": {
    "data_service": {
      "description": "Handles data operations: sync, list, summary, aggregate",
      "endpoints": {
        "sync": "/api/data/sync",
        "list": "/api/data/list",
        "aggregate": "/api/data/aggregate",
        "grouped-metrics": "/api/data/grouped-metrics",
        "periods": "/api/data/periods",
        "metrics": "/api/data/metrics/{account_type}"
      }
    },
    "ai_service": {
      "description": "Handles AI query operations",
      "endpoints": {
        "query": "/api/ai/query"
      }
    },
    "ai_analytics_service": {
      "description": "Handles AI-powered financial analytics",
      "endpoints": {
        "analytics_comprehensive": "/api/ai/analytics/comprehensive",
        "analytics_trends": "/api/ai/analytics/trends",
        "analytics_anomalies": "/api/ai/analytics/anomalies",
        "analytics_health_score": "/api/ai/analytics/health-score"
      }
    },
    "health_service": {
      "description": "Handles basic health checks",
      "endpoints": {
        "basic": "/api/health/",
        "basic_alt": "/api/health/basic"
      }
    }
  }
}
```

**Curl Example:**
```bash
curl -X GET "http://localhost:8000/"
```

---

## 🚨 Error Responses

All endpoints may return error responses in the following format:

```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "field": "period_start",
      "issue": "Invalid date format"
    }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common Error Codes
- `VALIDATION_ERROR`: Invalid request parameters
- `DATABASE_ERROR`: Database operation failed
- `AI_SERVICE_ERROR`: AI service unavailable
- `DATA_NOT_FOUND`: Requested data not found
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_SERVER_ERROR`: Unexpected server error

---

## 📚 Interactive Documentation

The API provides interactive documentation through Swagger UI:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- Explore all available endpoints
- Test API calls directly from the browser
- View request/response schemas
- Download OpenAPI specification

---

## 🔧 Rate Limiting

Currently, the API does not implement rate limiting. However, it's recommended to:
- Space requests appropriately
- Use pagination for large data sets
- Cache responses when possible

---

## 📝 Notes

1. **Date Formats**: All dates should be in YYYY-MM-DD format
2. **Currency**: All monetary values are returned in the base currency (USD)
3. **Pagination**: Use `limit` and `offset` parameters for paginated endpoints
4. **Context Management**: Use consistent `chat_id` for conversation context
5. **AI Queries**: Natural language queries work best with specific, clear questions

---

*This documentation is automatically generated and updated with the API. For the most current information, refer to the interactive documentation at `/docs`.*
