# AI Architecture Documentation

This document provides comprehensive documentation of the AI architecture, context management system, and analytics capabilities in the Financial Data Processing System.

## 🧠 AI Architecture Overview

The system implements a sophisticated AI architecture that combines natural language processing, SQL generation, and intelligent response formatting to provide powerful financial data analysis capabilities.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        AI Query Service                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Context       │  │   Internal Tool │  │   Analytics     │ │
│  │   Management    │  │   Orchestration │  │   Engine        │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Azure OpenAI Integration                     │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Query         │  │   Response      │  │   Analytics     │ │
│  │   Generation    │  │   Formatting   │  │   Processing    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Internal Tool Calling Architecture

The system implements a sophisticated internal tool calling architecture that orchestrates multiple specialized components to process natural language queries with enterprise-grade security and intelligent context management.

### Architecture Flow

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

### Internal Tool Chain Components
- **Purpose**: Orchestrate specialized AI tools for query processing
- **Input**: User query + enriched context + database schema metadata
- **Output**: Structured query plan with validated parameters
- **Components**:
  - `IntentAnalyzer`: Advanced intent classification and query understanding
  - `SchemaProvider`: Dynamic database schema injection with metadata
  - `QueryGenerator`: SQL generation with built-in security constraints
  - `SecurityValidator`: Multi-layer validation and sanitization engine

### Secure Database Interaction Layer
- **Purpose**: Execute validated queries with enterprise security measures
- **Input**: Sanitized SQL queries + validated parameters + schema constraints
- **Output**: Structured data results with metadata
- **Security Features**:
  - **Query Sanitization**: Advanced SQL injection prevention
  - **Parameter Validation**: Strict type checking and range validation
  - **Schema Enforcement**: Database schema validation and constraint enforcement
  - **Read-Only Enforcement**: Prevents any data modification operations
  - **Blotting Prevention**: Protection against data corruption and unauthorized access

## 🧩 Intelligent Context Management System

The system implements an advanced context management architecture that maintains conversation continuity through intelligent summarization, session persistence, and contextual relevance scoring.

### Context Architecture

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

### Context Components

#### 1. Chat Session Management
- **Purpose**: Persistent storage and management of conversation sessions
- **Features**:
  - **Session Persistence**: Long-term storage of chat sessions with metadata
  - **User Isolation**: Secure session isolation per user/chat_id
  - **Session Lifecycle**: Automatic session cleanup and archival
  - **Context Metadata**: Rich metadata tracking for each session

#### 2. Intelligent Context Summarization
- **Purpose**: Create dense, relevant summaries of conversation history
- **Features**:
  - **Semantic Summarization**: AI-powered extraction of key concepts and entities
  - **Relevance Scoring**: Dynamic relevance scoring for historical context
  - **Context Compression**: Intelligent compression while preserving critical information
  - **Temporal Awareness**: Time-aware context prioritization

#### 3. Advanced Relevance Scoring
- **Purpose**: Determine most relevant context for current queries
- **Features**:
  - **Semantic Similarity**: Advanced semantic matching between queries
  - **Temporal Weighting**: Recent context prioritized with intelligent decay
  - **Entity Recognition**: Financial entity extraction and matching
  - **Context Clustering**: Group related context for better retrieval

### Intelligent Context Flow

```
User Query → Context Intelligence → Semantic Analysis → Context Integration → Response Generation
     │              │                      │                      │                      │
     │              │                      │                      │                      │
     ▼              ▼                      ▼                      ▼                      ▼
┌─────────┐   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Natural │   │ Context         │  │ Semantic        │  │ Intelligent     │  │ Enhanced        │
│Language │   │ Intelligence    │  │ Entity          │  │ Context         │  │ Response        │
│ Query   │   │ Engine          │  │ Extraction      │  │ Fusion          │  │ Generation      │
└─────────┘   └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Advanced Context Reference Resolution

The system implements sophisticated context resolution through multiple intelligence layers:

#### Reference Intelligence Types
1. **Temporal Context Resolution**: "above period", "that quarter", "last month" with temporal reasoning
2. **Entity-Based References**: "that report", "same data source" with entity disambiguation
3. **Metric Context Resolution**: "that value", "same calculation" with metric correlation
4. **Comparative Context**: "compared to above", "vs previous" with comparative analysis

#### Intelligent Resolution Process
```
Context Detection → Semantic Analysis → Entity Extraction → Context Fusion → Query Enhancement
        │                    │                │                    │                    │
        │                    │                │                    │                    │
        ▼                    ▼                ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Advanced        │  │ Semantic        │  │ Financial       │  │ Context         │  │ Enhanced        │
│ Reference       │  │ Entity          │  │ Entity          │  │ Intelligence    │  │ Query           │
│ Detection       │  │ Recognition     │  │ Extraction      │  │ Fusion          │  │ Construction    │
└─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Chat Session Architecture

#### Session Persistence Layer
- **Chat Sessions Table**: Comprehensive session metadata with lifecycle management
- **Message History**: Rich message storage with context embeddings
- **Context Summaries**: Intelligent summaries with relevance scoring
- **Session Analytics**: Usage patterns and context effectiveness metrics

#### Context Intelligence Features
- **Dynamic Context Window**: Adaptive context window sizing based on query complexity
- **Context Relevance Scoring**: Multi-factor relevance scoring for historical context
- **Semantic Context Clustering**: Group related context for improved retrieval
- **Temporal Context Weighting**: Intelligent time-based context prioritization

## 🔍 AI Analytics Architecture

The analytics system provides advanced AI-powered financial analysis capabilities.

### Analytics Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    Analytics Service Layer                      │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Trend         │  │   Anomaly       │  │   Health        │ │
│  │   Analyzer      │  │   Detector      │  │   Scorer        │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Financial Data Processing                    │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Data          │  │   Pattern        │  │   Statistical   │ │
│  │   Aggregation   │  │   Recognition    │  │   Analysis      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 1. Trend Analysis
- **Purpose**: Identify patterns and trends in financial data
- **Capabilities**:
  - Linear trend detection
  - Seasonal pattern recognition
  - Growth rate calculation
  - Forecasting
- **AI Integration**: Uses LLM for pattern interpretation and insight generation

### 2. Anomaly Detection
- **Purpose**: Identify unusual patterns and outliers
- **Capabilities**:
  - Statistical outlier detection
  - Pattern deviation analysis
  - Severity classification
  - Root cause suggestions
- **AI Integration**: LLM analyzes anomalies and suggests explanations

### 3. Financial Health Scoring
- **Purpose**: Comprehensive financial health assessment
- **Capabilities**:
  - Multi-dimensional scoring
  - Risk assessment
  - Recommendation generation
  - Trend-based scoring
- **AI Integration**: LLM provides contextual scoring and recommendations

## 🎯 LLM Integration Architecture

### Azure OpenAI Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                    LLM Service Layer                           │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Singleton     │  │   Token         │  │   Error         │ │
│  │   Management    │  │   Management    │  │   Handling      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Azure OpenAI API                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   GPT-4         │  │   GPT-3.5       │  │   Embeddings    │ │
│  │   Deployment    │  │   Deployment    │  │   Service       │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### LLM Service Features
- **Singleton Pattern**: Ensures single instance across the application
- **Model Management**: Supports multiple model deployments
- **Token Management**: Efficient context window management
- **Error Handling**: Robust error handling and fallback mechanisms
- **Configuration**: Environment-based configuration

### Prompt Engineering

#### Query Generation Prompts
- **Schema Integration**: Database schema embedded in prompts
- **Context Integration**: Historical conversation context
- **Safety Constraints**: SQL injection prevention
- **Intent Classification**: Structured intent recognition

#### Response Formatting Prompts
- **Data Integration**: Query results embedded in prompts
- **Context Awareness**: Historical context for consistency
- **Business Language**: Professional financial terminology
- **Insight Generation**: AI-generated business insights

## 🔧 Database Schema for AI

### Core Tables

#### 1. Finance Transactions
```sql
CREATE TABLE finance_transactions (
    transaction_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    value DECIMAL(15,2),
    period_start DATE,
    period_end DATE,
    source_id INTEGER,
    created_at TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);
```

#### 2. Accounts
```sql
CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    type INTEGER,  -- Enum: Revenue=1, COGS=2, Expense=3, Tax=4, Derived=5
    sub_type VARCHAR(100),
    currency INTEGER,  -- Enum: USD=1, EUR=2, etc.
    created_at TIMESTAMP
);
```

#### 3. Chat Sessions
```sql
CREATE TABLE chat_sessions (
    chat_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    created_at TIMESTAMP,
    last_activity TIMESTAMP,
    context_summary TEXT
);
```

#### 4. Chat Messages
```sql
CREATE TABLE chat_messages (
    message_id INTEGER PRIMARY KEY,
    chat_id VARCHAR(255),
    message_type VARCHAR(50),  -- 'user' or 'assistant'
    content TEXT,
    query_intent VARCHAR(100),
    data_points JSON,
    prompt TEXT,
    llm_response TEXT,
    summary TEXT,
    token_count INTEGER,
    created_at TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES chat_sessions(chat_id)
);
```

## 🚀 Performance Optimization

### Context Management Optimization
- **Token Limits**: Configurable token limits per context window
- **Context Summarization**: Dense summarization to preserve key information
- **Priority System**: Recent context prioritized over older context
- **Caching**: Context caching for frequently accessed conversations

### Query Optimization
- **SQL Validation**: Pre-execution validation prevents errors
- **Query Caching**: Cached results for repeated queries
- **Connection Pooling**: Efficient database connection management
- **Indexing**: Optimized database indexes for common queries

### LLM Optimization
- **Batch Processing**: Batch multiple requests when possible
- **Response Streaming**: Stream responses for better user experience
- **Model Selection**: Appropriate model selection based on complexity
- **Error Recovery**: Graceful error handling and recovery

## 🔒 Enterprise Security Architecture

### Database Security Framework

#### Query Sanitization Engine
- **Advanced SQL Injection Prevention**: Multi-layer validation with pattern recognition
- **Parameter Binding**: Secure parameter binding with type enforcement
- **Query Structure Validation**: Syntax and structure validation before execution
- **Malicious Pattern Detection**: Real-time detection of suspicious query patterns

#### Data Integrity Protection
- **Read-Only Enforcement**: Strict enforcement of read-only operations
- **Schema Validation**: Dynamic schema validation with constraint enforcement
- **Data Blotting Prevention**: Protection against data corruption and unauthorized modifications
- **Access Control**: Role-based access control with granular permissions

#### Security Validation Layers
```
Query Input → Syntax Validation → Parameter Sanitization → Schema Validation → Execution
     │              │                      │                      │                    │
     │              │                      │                      │                    │
     ▼              ▼                      ▼                      ▼                    ▼
┌─────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Raw Query   │  │ Syntax          │  │ Parameter       │  │ Schema          │  │ Secure          │
│ Input       │  │ Validation      │  │ Sanitization    │  │ Enforcement     │  │ Execution       │
└─────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Database Schema Security

#### Schema Injection Protection
- **Dynamic Schema Provision**: Secure schema metadata injection with validation
- **Schema Constraint Enforcement**: Strict enforcement of database constraints
- **Metadata Validation**: Validation of schema metadata before injection
- **Access Pattern Analysis**: Analysis of query patterns for security compliance

### Advanced Security Features

#### Context Security
- **Session Isolation**: Secure chat session isolation per user
- **Context Encryption**: Sensitive context data encryption at rest
- **Access Control**: Granular access control with role-based permissions
- **Audit Logging**: Comprehensive security audit logging

#### API Security Framework
- **Input Validation**: Multi-layer input validation with sanitization
- **Rate Limiting**: Intelligent rate limiting with adaptive thresholds
- **CORS Configuration**: Secure cross-origin resource sharing
- **Error Handling**: Secure error handling without information leakage

#### Data Protection
- **Encryption at Rest**: Sensitive data encryption with key management
- **Transit Security**: Secure data transmission with TLS encryption
- **Data Anonymization**: Context data anonymization for privacy
- **Compliance**: GDPR and financial data compliance measures

## 📊 Monitoring and Observability

### AI-Specific Metrics
- **Query Success Rate**: Percentage of successful AI queries
- **Response Time**: Average response time for AI queries
- **Token Usage**: Token consumption tracking
- **Context Accuracy**: Context resolution accuracy

### System Metrics
- **Database Performance**: Query execution times
- **API Performance**: Endpoint response times
- **Error Rates**: Error rates by component
- **Resource Usage**: CPU, memory, and storage usage

### Logging Strategy
- **Structured Logging**: JSON-formatted logs
- **Log Levels**: Appropriate log levels for different components
- **Context Preservation**: Log context preservation across components
- **Performance Logging**: Detailed performance metrics

## 🔮 Future Enhancements

### Planned Improvements
1. **Multi-Model Support**: Support for multiple LLM providers
2. **Advanced Analytics**: More sophisticated analytics algorithms
3. **Real-Time Processing**: Real-time data processing capabilities
4. **Enhanced Context**: More sophisticated context management
5. **Custom Models**: Fine-tuned models for financial domain

### Scalability Considerations
1. **Horizontal Scaling**: Multi-instance deployment support
2. **Database Scaling**: Database sharding and replication
3. **Caching Layer**: Distributed caching for better performance
4. **Load Balancing**: Intelligent load balancing for AI services
5. **Microservices**: Potential microservices architecture

---

*This documentation provides a comprehensive overview of the AI architecture. For implementation details, refer to the source code in the `src/handler/ai/` directory.*
