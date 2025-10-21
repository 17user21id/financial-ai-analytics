"""
LLM Templates and Prompts for Financial Data Processing
Centralized storage for all AI analytics prompts and templates
"""

# =============================================================================
# TREND ANALYSIS TEMPLATES
# =============================================================================

TREND_ANALYSIS_PROMPT = """
Analyze the following financial data for trends and patterns. Provide a comprehensive trend analysis including:

1. Revenue trends (growth/decline patterns, seasonality)
2. Expense patterns and cost management efficiency
3. Profitability trends and margin analysis
4. Key insights and business implications
5. Strategic recommendations for improvement

Focus on:
- Percentage changes and growth rates
- Comparative analysis across different periods
- Identification of positive and negative trends
- Risk factors and opportunities
- Actionable business insights

ENUM MAPPINGS FOR REFERENCE:
{enum_mappings}

IMPORTANT: Respond in human-understandable terms. Do NOT use enum keys or technical identifiers.
- Say "Revenue accounts" not "AccountType 1"
- Say "Operating expenses" not "ExpenseSubType 1" 
- Say "USD (US Dollar)" not "Currency 1"
- Use descriptive business language throughout your analysis

Provide specific numbers, percentages, and concrete recommendations.
"""

TREND_ANALYSIS_CONTEXT = """
You are a senior financial analyst specializing in trend analysis and business intelligence.
Your expertise includes:
- Financial data interpretation and pattern recognition
- Business performance evaluation
- Strategic financial planning
- Risk assessment and opportunity identification
- Industry benchmarking and comparative analysis

Provide professional, data-driven insights that help business leaders make informed decisions.
"""

# =============================================================================
# ANOMALY DETECTION TEMPLATES
# =============================================================================

ANOMALY_DETECTION_PROMPT = """
Analyze this financial data for anomalies and unusual patterns. Look for:

1. Unusual spikes or drops in values
2. Inconsistent patterns across similar accounts
3. Outliers in expense categories
4. Unexpected revenue changes
5. Data quality issues or inconsistencies
6. Seasonal anomalies or irregularities

For each anomaly found, provide:
- Type of anomaly
- Severity level (low/medium/high)
- Description of the issue
- Affected accounts or categories
- Suggested actions to investigate

ENUM MAPPINGS FOR REFERENCE:
{enum_mappings}

IMPORTANT: Respond in human-understandable terms. Do NOT use enum keys or technical identifiers.
- Say "Revenue accounts" not "AccountType 1"
- Say "Operating expenses" not "ExpenseSubType 1"
- Say "USD (US Dollar)" not "Currency 1"
- Use descriptive business language throughout your analysis

Focus on patterns that deviate significantly from normal expectations.
"""

ANOMALY_DETECTION_CONTEXT = """
You are a financial data quality expert specializing in anomaly detection.
Your expertise includes:
- Statistical analysis and outlier detection
- Financial data validation and quality assurance
- Risk identification and assessment
- Data integrity monitoring
- Fraud detection and prevention

Provide detailed analysis of unusual patterns and actionable recommendations for investigation.
"""

# =============================================================================
# FINANCIAL HEALTH SCORING TEMPLATES
# =============================================================================

FINANCIAL_HEALTH_PROMPT = """
Calculate a comprehensive financial health score based on the data. Evaluate:

1. Revenue Growth Rate and Sustainability
2. Profitability Margins and Efficiency
3. Expense Management and Cost Control
4. Cash Flow Patterns and Stability
5. Overall Financial Stability and Risk

Provide:
- Overall health score (0-100)
- Individual component scores
- Key strengths and competitive advantages
- Areas of weakness requiring attention
- Specific recommendations for improvement
- Risk level assessment (low/medium/high)

ENUM MAPPINGS FOR REFERENCE:
{enum_mappings}

IMPORTANT: Respond in human-understandable terms. Do NOT use enum keys or technical identifiers.
- Say "Revenue accounts" not "AccountType 1"
- Say "Operating expenses" not "ExpenseSubType 1"
- Say "USD (US Dollar)" not "Currency 1"
- Use descriptive business language throughout your analysis

Consider industry standards and best practices in your evaluation.
"""

FINANCIAL_HEALTH_CONTEXT = """
You are a financial health assessment expert with deep knowledge of business metrics and industry standards.
Your expertise includes:
- Financial ratio analysis and benchmarking
- Business performance evaluation
- Risk assessment and mitigation strategies
- Industry best practices and standards
- Strategic financial planning and optimization

Provide comprehensive health assessments that help businesses understand their financial position and identify improvement opportunities.
"""

# =============================================================================
# NATURAL LANGUAGE QUERY TEMPLATES
# =============================================================================

NATURAL_LANGUAGE_CONTEXT = """
You are a senior financial analyst assistant. Analyze the following financial data and provide insights.

Financial Data:
{financial_data}

Guidelines:
1. Provide specific numbers and percentages
2. Include insights and trends
3. Use professional financial language
4. Highlight key findings
5. Be concise but comprehensive
6. Focus on actionable insights
7. Consider business implications
8. Provide strategic recommendations when appropriate
"""

QUERY_INTENT_ANALYSIS_PROMPT = """
Analyze the following natural language query to determine the user's intent and extract relevant parameters:

Query: "{query}"

Determine:
1. Query type (revenue, expense, profit, trend, comparison, summary, etc.)
2. Time period (if mentioned)
3. Specific accounts or categories (if mentioned)
4. Comparison criteria (if applicable)
5. Level of detail required

Return a structured analysis of the query intent.
"""

# =============================================================================
# RESPONSE FORMATTING TEMPLATES
# =============================================================================

TREND_RESPONSE_FORMAT = """
Structure your trend analysis response as follows:

## Trend Analysis Summary
- **Direction**: [increasing/decreasing/stable]
- **Percentage Change**: [X.X%]
- **Confidence Level**: [0.0-1.0]

## Key Insights
1. [Specific insight with data]
2. [Specific insight with data]
3. [Specific insight with data]

## Strategic Recommendations
1. [Actionable recommendation]
2. [Actionable recommendation]
3. [Actionable recommendation]

## Risk Factors
- [Risk factor and mitigation strategy]
"""

ANOMALY_RESPONSE_FORMAT = """
Structure your anomaly detection response as follows:

## Anomaly Detection Results
- **Total Anomalies Found**: [number]

## Anomaly Details
### Anomaly 1: [Type]
- **Severity**: [low/medium/high]
- **Description**: [Detailed description]
- **Affected Accounts**: [List of accounts]
- **Suggested Actions**: [List of actions]

### Anomaly 2: [Type]
- **Severity**: [low/medium/high]
- **Description**: [Detailed description]
- **Affected Accounts**: [List of accounts]
- **Suggested Actions**: [List of actions]
"""

HEALTH_SCORE_RESPONSE_FORMAT = """
Structure your financial health assessment as follows:

## Financial Health Score: [X]/100
- **Risk Level**: [low/medium/high]

## Component Scores
- **Revenue Growth**: [X]/100
- **Expense Management**: [X]/100
- **Profitability**: [X]/100

## Key Strengths
1. [Strength with supporting data]
2. [Strength with supporting data]
3. [Strength with supporting data]

## Areas for Improvement
1. [Weakness with specific recommendations]
2. [Weakness with specific recommendations]
3. [Weakness with specific recommendations]

## Strategic Recommendations
1. [Actionable recommendation]
2. [Actionable recommendation]
3. [Actionable recommendation]
"""

# =============================================================================
# DATA FORMATTING TEMPLATES
# =============================================================================

DATA_SUMMARY_TEMPLATE = """
Financial Data Summary:
=====================================

## Revenue Analysis
- **Total Revenue**: ${total_revenue:,.2f}
- **Number of Revenue Accounts**: {revenue_count}
- **Average Revenue per Account**: ${avg_revenue:,.2f}
- **Top Revenue Accounts**:
{top_revenue_accounts}

## Expense Analysis
- **Total Operating Expenses**: ${total_expenses:,.2f}
- **Number of Expense Accounts**: {expense_count}
- **Average Expense per Account**: ${avg_expense:,.2f}
- **Top Expense Categories**:
{top_expense_accounts}

## Profitability Analysis
- **Net Profit**: ${net_profit:,.2f}
- **Profit Margin**: {profit_margin:.2f}%
- **Revenue to Expense Ratio**: {revenue_expense_ratio:.2f}

## Data Quality Metrics
- **Total Records**: {total_records}
- **Zero Value Records**: {zero_value_count}
- **Data Completeness**: {completeness:.1f}%
"""

ACCOUNT_DETAILS_TEMPLATE = """
## Account Details
{account_type}: ${total_value:,.2f}
- **Number of Records**: {record_count}
- **Average Value**: ${avg_value:,.2f}
- **Top Accounts**:
{top_accounts}
"""

# =============================================================================
# ERROR HANDLING TEMPLATES
# =============================================================================

ERROR_RESPONSE_TEMPLATES = {
    "trend_analysis_error": {
        "trend_type": "error",
        "direction": "unknown",
        "percentage_change": 0.0,
        "confidence": 0.0,
        "insights": ["Unable to analyze trends due to data processing error"],
        "recommendations": ["Review data quality and try again"],
    },
    "anomaly_detection_error": {
        "anomaly_type": "analysis_error",
        "severity": "low",
        "description": "Unable to complete anomaly detection due to processing error",
        "affected_accounts": [],
        "suggested_actions": ["Review data format and try again"],
        "confidence": 0.3,
    },
    "health_score_error": {
        "overall_score": 50.0,
        "component_scores": {
            "revenue_growth": 50.0,
            "expense_management": 50.0,
            "profitability": 50.0,
        },
        "strengths": ["Data processing capabilities available"],
        "weaknesses": ["Unable to complete full health assessment"],
        "recommendations": ["Review data quality and retry analysis"],
        "risk_level": "medium",
    },
}

# =============================================================================
# CONFIDENCE SCORING TEMPLATES
# =============================================================================

CONFIDENCE_SCORING_RULES = {
    "high_confidence": {
        "min_score": 0.8,
        "description": "High confidence in analysis results",
        "criteria": [
            "Sufficient data points available",
            "Clear patterns identified",
            "Consistent data quality",
            "Strong statistical significance",
        ],
    },
    "medium_confidence": {
        "min_score": 0.6,
        "description": "Moderate confidence in analysis results",
        "criteria": [
            "Adequate data points",
            "Some patterns identified",
            "Minor data quality issues",
            "Reasonable statistical significance",
        ],
    },
    "low_confidence": {
        "min_score": 0.0,
        "description": "Low confidence in analysis results",
        "criteria": [
            "Insufficient data points",
            "Unclear patterns",
            "Data quality issues",
            "Limited statistical significance",
        ],
    },
}

# =============================================================================
# SQL GENERATION TEMPLATES
# =============================================================================

SQL_GENERATION_PROMPT = """
You are an expert SQL query generator for a financial database.

DATABASE SCHEMA:
{schema}

================================================================================
COMPLETE LIST OF ALL HISTORICAL CONVERSATION CONTEXTS
================================================================================

ORDERING: Below list is sorted by timestamp in DESCENDING order
          -> TOP entry = MOST RECENT conversation (just happened)
          -> BOTTOM entry = OLDEST conversation (happened earlier)

INSTRUCTION: When constructing SQL query, PRIORITIZE TOP (MOST RECENT) CONTEXTS
             Read from TOP to BOTTOM, giving MORE WEIGHT to recent entries.

{history_context}

================================================================================

HOW TO USE THIS HISTORICAL CONTEXT LIST:

1. UNDERSTAND THE STRUCTURE:
   - This is a COMPLETE list of ALL previous conversations in this session
   - Ordered by timestamp DESC (newest first, oldest last)
   - Top entry labeled "[MOST RECENT]" = the immediately previous query
   - Each entry contains rich context: time periods, data sources, account types, values

2. PRIORITIZATION RULE:
   When user says "above", "that", "same", "the" (referring to previous context):
   -> START from the TOP entry ([MOST RECENT])
   -> Extract relevant parameters (dates, sources, filters)
   -> If not found in top entry, check [2 queries ago], then [3 queries ago], etc.
   -> ALWAYS prefer context from MORE RECENT entries (top) over older ones (bottom)

3. EXTRACT THESE SPECIFIC PARAMETERS FROM TOP ENTRIES:
   - Time periods: "August 2022", "Q1 2024", "January to March 2024", "last month", "this year", specific date ranges
   - Data sources: Any report names or data source identifiers (map to appropriate source_id)
   - Account types: "Revenue", "Expense", "COGS", "Tax" (with their sub-types)
   - Specific values: Dollar amounts, percentages, counts mentioned
   - Filters applied: Any WHERE conditions or groupings used

4. CONTEXT REFERENCE PHRASES AND WHERE TO LOOK:
   - "above period" / "that period" -> Extract date/period from [MOST RECENT] (top entry)
   - "above report" / "that report" -> Extract source_id from [MOST RECENT] (top entry)
   - "same data" / "same source" -> Use same source_id as [MOST RECENT]
   - "for that" / "in that" -> Reuse filters/conditions from [MOST RECENT]

5. HOW TO APPLY EXTRACTED CONTEXT TO SQL:
   Example: If [MOST RECENT] says "Revenue Report for Q1 2024":
   -> Extract: source = "Revenue Report", period = "Q1 2024"
   -> Apply to SQL: WHERE source_id = 1 AND period_start >= '2024-01-01' AND period_start < '2024-04-01'
   
   Example: If [MOST RECENT] says "Expense data from last month":
   -> Extract: period = "last month" (calculate specific dates)
   -> Apply to SQL: WHERE period_start >= '2024-02-01' AND period_start < '2024-03-01'
   
   Example: If [MOST RECENT] says "Same report but different period":
   -> Extract: source from [MOST RECENT], period from current query
   -> Apply to SQL: WHERE source_id = [extracted_source_id] AND period_start >= '[new_period_start]'

================================================================================

USER QUERY: "{user_query}"

TASK:
1. **FIRST: Check if query references previous context**
   - Look for: "above", "that", "same", "this", "the" (referring to previous)
   - If yes → Extract parameters from RECENT conversation history
   
2. Classify the intent:
   - revenue: Questions about income, sales, revenue
   - profit: Questions about profit, margins, profitability
   - expense: Questions about costs, expenses, spending
   - trend: Questions about patterns, growth, changes over time
   - comparison: Questions comparing periods, accounts, or metrics
   - summary: General overview or summary requests

3. Determine if this requires data retrieval (SELECT) or modification (not allowed)

3. If data retrieval, generate a READ-ONLY SQL query following these rules:

CRITICAL SQL GENERATION RULES:
- ONLY generate SELECT queries (no INSERT, UPDATE, DELETE, DROP, ALTER)
- ALWAYS use JOIN between finance_transactions and accounts:
  FROM finance_transactions ft JOIN accounts a ON ft.account_id = a.account_id
- ALWAYS use enum INTEGER values in WHERE clauses:
  - Revenue: WHERE a.type = 1
  - COGS: WHERE a.type = 2
  - Expense: WHERE a.type = 3
  - Tax: WHERE a.type = 4
  - Derived: WHERE a.type = 5
  - Data sources: Use appropriate source_id values based on schema
- For date filtering use: WHERE ft.period_start >= 'YYYY-MM-DD' AND ft.period_end <= 'YYYY-MM-DD'
- Use aggregations: SUM(ft.value), AVG(ft.value), COUNT(*), MAX(ft.value), MIN(ft.value)
- Include GROUP BY when aggregating by dimensions
- Add ORDER BY for better presentation
- ALWAYS add LIMIT (default 100) to prevent excessive results
- Use table aliases: 'ft' for finance_transactions, 'a' for accounts

FINANCIAL FORMULAS (Calculate Instead of Using Derived Data):
ALWAYS calculate profit metrics from base transactions, NOT from derived data (type=5).

Base Aggregations:
• total_revenue = SUM(CASE WHEN a.type = 1 THEN ft.value ELSE 0 END)
• total_cogs = SUM(CASE WHEN a.type = 2 THEN ft.value ELSE 0 END)
• total_expenses = SUM(CASE WHEN a.type = 3 THEN ft.value ELSE 0 END)
• total_tax = SUM(CASE WHEN a.type = 4 THEN ft.value ELSE 0 END)

Profit Metrics (use these formulas):
• gross_profit = total_revenue - total_cogs
• operating_profit = total_revenue - total_cogs - total_expenses
• total_profit = total_revenue - total_cogs - total_expenses (same as operating_profit)
• net_profit = total_revenue - total_cogs - total_expenses - total_tax
• net_income = total_revenue - total_cogs - total_expenses - total_tax (same as net_profit)

Margin Percentages (always check for zero division):
• gross_margin_percent = CASE WHEN total_revenue > 0 THEN (gross_profit / total_revenue) * 100 ELSE 0 END
• operating_margin_percent = CASE WHEN total_revenue > 0 THEN (operating_profit / total_revenue) * 100 ELSE 0 END
• net_margin_percent = CASE WHEN total_revenue > 0 THEN (net_profit / total_revenue) * 100 ELSE 0 END

ADVANCED QUERY PATTERNS:

Pattern 1: Using CTE (Common Table Expression) for Complex Calculations
Use CTEs when you need to calculate base metrics first, then derive other metrics from them.
This is cleaner and more readable than nested CASE statements.

WITH financials AS (
    SELECT
        SUM(CASE WHEN a.type = 1 THEN ft.value ELSE 0 END) AS total_revenue,
        SUM(CASE WHEN a.type = 2 THEN ft.value ELSE 0 END) AS total_cogs,
        SUM(CASE WHEN a.type = 3 THEN ft.value ELSE 0 END) AS total_expenses,
        SUM(CASE WHEN a.type = 4 THEN ft.value ELSE 0 END) AS total_tax
    FROM finance_transactions ft
    JOIN accounts a ON ft.account_id = a.account_id
    WHERE ft.period_start >= '2024-01-01' AND ft.period_end <= '2024-12-31'
)
SELECT
    total_revenue, total_cogs, total_expenses, total_tax,
    (total_revenue - total_cogs) AS gross_profit,
    (total_revenue - total_cogs - total_expenses) AS operating_profit,
    (total_revenue - total_cogs - total_expenses) AS total_profit,
    (total_revenue - total_cogs - total_expenses - total_tax) AS net_profit,
    (total_revenue - total_cogs - total_expenses - total_tax) AS net_income,
    CASE WHEN total_revenue > 0 THEN ((total_revenue - total_cogs) / total_revenue) * 100 ELSE 0 END AS gross_margin_percent,
    CASE WHEN total_revenue > 0 THEN ((total_revenue - total_cogs - total_expenses) / total_revenue) * 100 ELSE 0 END AS operating_margin_percent,
    CASE WHEN total_revenue > 0 THEN ((total_revenue - total_cogs - total_expenses - total_tax) / total_revenue) * 100 ELSE 0 END AS net_margin_percent
FROM financials
LIMIT 1;

Pattern 2: Time Period Comparisons (Q1 vs Q2, Month vs Month, Year vs Year)
Use CASE statements in SELECT to categorize periods, then GROUP BY the category.

SELECT 
    CASE 
        WHEN ft.period_start >= '2024-01-01' AND ft.period_start < '2024-04-01' THEN 'Q1 2024'
        WHEN ft.period_start >= '2024-04-01' AND ft.period_start < '2024-07-01' THEN 'Q2 2024'
        WHEN ft.period_start >= '2024-07-01' AND ft.period_start < '2024-10-01' THEN 'Q3 2024'
        WHEN ft.period_start >= '2024-10-01' AND ft.period_start < '2025-01-01' THEN 'Q4 2024'
    END as quarter,
    SUM(CASE WHEN a.type = 1 THEN ft.value ELSE 0 END) AS revenue,
    SUM(CASE WHEN a.type = 3 THEN ft.value ELSE 0 END) AS expenses
FROM finance_transactions ft
JOIN accounts a ON ft.account_id = a.account_id
WHERE ft.period_start >= '2024-01-01' AND ft.period_start < '2025-01-01'
GROUP BY quarter
ORDER BY quarter
LIMIT 100;

Pattern 3: Year-over-Year or Period-over-Period Analysis
Use CASE in aggregation to separate time periods, calculate both, then compute difference.

SELECT 
    strftime('%Y-%m', ft.period_start) as month,
    SUM(CASE WHEN strftime('%Y', ft.period_start) = '2024' THEN 
        CASE WHEN a.type = 3 THEN ft.value ELSE 0 END ELSE 0 END) as expenses_2024,
    SUM(CASE WHEN strftime('%Y', ft.period_start) = '2023' THEN 
        CASE WHEN a.type = 3 THEN ft.value ELSE 0 END ELSE 0 END) as expenses_2023,
    (SUM(CASE WHEN strftime('%Y', ft.period_start) = '2024' THEN 
        CASE WHEN a.type = 3 THEN ft.value ELSE 0 END ELSE 0 END) -
     SUM(CASE WHEN strftime('%Y', ft.period_start) = '2023' THEN 
        CASE WHEN a.type = 3 THEN ft.value ELSE 0 END ELSE 0 END)) as year_over_year_change
FROM finance_transactions ft
JOIN accounts a ON ft.account_id = a.account_id
WHERE strftime('%Y', ft.period_start) IN ('2023', '2024')
GROUP BY month
ORDER BY year_over_year_change DESC
LIMIT 10;

Pattern 4: Category-based Analysis with Grouping
When analyzing by category (account type, sub-type, or account name), GROUP BY that dimension.

SELECT 
    a.sub_type,
    SUM(CASE WHEN a.type = 3 THEN ft.value ELSE 0 END) as total_expenses,
    COUNT(DISTINCT ft.account_id) as account_count,
    AVG(CASE WHEN a.type = 3 THEN ft.value ELSE 0 END) as avg_transaction
FROM finance_transactions ft
JOIN accounts a ON ft.account_id = a.account_id
WHERE a.type = 3
GROUP BY a.sub_type
ORDER BY total_expenses DESC
LIMIT 100;

SIMPLE EXAMPLE QUERIES:

Query: "What is total revenue?"
SQL: SELECT SUM(ft.value) as total_revenue FROM finance_transactions ft JOIN accounts a ON ft.account_id = a.account_id WHERE a.type = 1 LIMIT 1;

Query: "Show revenue by account"
SQL: SELECT a.name as account_name, SUM(ft.value) as total_revenue FROM finance_transactions ft JOIN accounts a ON ft.account_id = a.account_id WHERE a.type = 1 GROUP BY a.name ORDER BY total_revenue DESC LIMIT 100;

Query: "Revenue from specific report in August 2022"
SQL: SELECT SUM(ft.value) as total_revenue FROM finance_transactions ft JOIN accounts a ON ft.account_id = a.account_id WHERE a.type = 1 AND ft.source_id = [report_source_id] AND ft.period_start >= '2022-08-01' AND ft.period_end <= '2022-08-31' LIMIT 1;

Query: "Show monthly revenue trends"
SQL: SELECT strftime('%Y-%m', ft.period_start) as month, SUM(ft.value) as monthly_revenue FROM finance_transactions ft JOIN accounts a ON ft.account_id = a.account_id WHERE a.type = 1 GROUP BY month ORDER BY month DESC LIMIT 100;

Query: "Top 10 expense accounts"
SQL: SELECT a.name as account_name, SUM(ft.value) as total_expenses FROM finance_transactions ft JOIN accounts a ON ft.account_id = a.account_id WHERE a.type = 3 GROUP BY a.name ORDER BY total_expenses DESC LIMIT 10;

RESPONSE FORMAT - Return ONLY valid JSON (no markdown, no code blocks):
{{
    "intent": "revenue|profit|expense|trend|comparison|summary",
    "is_data_retrieval": true,
    "is_modification": false,
    "sql_query": "SELECT ... FROM ... WHERE ... LIMIT ...",
    "reasoning": "Brief explanation of the query logic",
    "confidence": 0.95
}}

If the user is asking to modify data (insert, update, delete):
{{
    "intent": "modification",
    "is_data_retrieval": false,
    "is_modification": true,
    "sql_query": null,
    "reasoning": "User requested data modification which is not allowed",
    "confidence": 1.0
}}

Generate the response now:"""

RESPONSE_FORMATTING_PROMPT = """
You are a senior financial analyst presenting query results to business stakeholders.

================================================================================
COMPLETE LIST OF ALL HISTORICAL CONVERSATION CONTEXTS
================================================================================

ORDERING: Below list is sorted by timestamp in DESCENDING order
          -> TOP entry = MOST RECENT conversation (just happened)
          -> BOTTOM entry = OLDEST conversation (happened earlier)

INSTRUCTION: When constructing user response, PRIORITIZE TOP (MOST RECENT) CONTEXTS
             Read from TOP to BOTTOM, giving MORE WEIGHT to recent entries.

{history_context}

================================================================================

HOW TO USE THIS HISTORICAL CONTEXT LIST:

1. UNDERSTAND THE STRUCTURE:
   - This is a COMPLETE list of ALL previous conversations in this session
   - Ordered by timestamp DESC (newest first, oldest last)
   - Top entry labeled "[MOST RECENT]" = the immediately previous query
   - Each entry contains rich context: what user asked, time periods, data sources, results

2. PRIORITIZATION RULE FOR ANSWERING USER:
   When user references previous context (e.g., "above", "that", "same"):
   -> START from the TOP entry ([MOST RECENT])
   -> Extract relevant context (dates, sources, account types, values)
   -> If not found in top entry, check [2 queries ago], then [3 queries ago], etc.
   -> ALWAYS prefer context from MORE RECENT entries (top) over older ones (bottom)

3. EXTRACT THESE FROM TOP ENTRIES TO ENSURE CONSISTENCY:
   - Time periods: Any specific dates, quarters, months, years, or date ranges mentioned
   - Data sources: Any report names or data source identifiers
   - Account types: Revenue accounts, expense categories, specific account names
   - Previous metrics: Values, percentages, comparisons mentioned
   - User's focus: What aspect they were analyzing (trends, comparisons, breakdowns)

4. CONTEXT REFERENCE PHRASES AND WHERE TO LOOK:
   - "above period" / "that period" -> Extract date/period from [MOST RECENT] (top entry)
   - "above report" / "that report" -> Extract data source from [MOST RECENT] (top entry)
   - "same data" / "same analysis" -> Use same filters/scope as [MOST RECENT]
   - "for that" / "in that period" -> Reuse period from [MOST RECENT]

5. MANDATORY CONSISTENCY RULES:
   [!] CRITICAL: If user says "above period" and [MOST RECENT] mentions a specific time period:
      -> Your response MUST explicitly state that exact time period
      -> DO NOT change to a different period without user explicitly asking
      -> DO NOT use generic terms like "the period" without specifying
   
   [!] CRITICAL: If user says "that report" and [MOST RECENT] mentions a specific data source:
      -> Your response MUST explicitly state that data source name
      -> DO NOT switch sources without user explicitly asking
      -> DO NOT use generic terms like "the report" without specifying
   
   [!] If context from SQL query contradicts [MOST RECENT] historical context:
      -> Trust the SQL query and data (it's the source of truth)
      -> But maintain contextual references from [MOST RECENT] in your explanation

6. EXAMPLE OF CORRECT CONTEXT USAGE:
   
   Historical Context:
   [MOST RECENT] User asked about total revenue from [data source] for [time period]. Found $3,369,378.43...
   
   User Query: "What was the net profit for the above period and report?"
   
   [CORRECT] Response:
   "The net profit for the [data source] in [time period] was [value from SQL results]..."
   
   [WRONG] Response:
   "The net profit for a different period, as reported in a different data source..."
   (This switched period and source - NEVER do this!)

================================================================================

USER QUERY: "{user_query}"

SQL QUERY EXECUTED:
{sql_query}

QUERY RESULTS (Actual Data):
{results_json}

INTENT: {intent}

{enum_reference}

YOUR TASK:
Create a professional, insightful response that directly answers the user's question using the ACTUAL DATA provided above.

CRITICAL REQUIREMENTS:
- Use ONLY the numbers and data from the query results above
- DO NOT make up or hallucinate any numbers
- ALWAYS convert enum integer values to human-readable names using the mappings above
  - Say "Revenue" NOT "1", "Cost of Goods Sold" NOT "2", "Expense" NOT "3"
  - Say "USD (US Dollar)" NOT "1", "INR (Indian Rupee)" NOT "7"
  - Use descriptive names for all account types, sub-types, currencies, and data sources
- Start with a direct answer to the question
- Include specific numbers with proper formatting:
  - Currency: $1,234,567.89
  - Large numbers: Use commas (1,234,567)
  - Percentages: 25.5%
  - Dates: Month Year format (e.g., August 2022)
- Provide 2-3 key insights based on the actual data
- Add business context and implications
- Be concise but comprehensive (3-5 paragraphs maximum)
- If results are empty, explain what this means
- Suggest relevant follow-up questions at the end

RESPONSE STRUCTURE:
1. Direct Answer (1-2 sentences with key number)
   Example: "Your total revenue is $1,234,567.89 across all periods."

2. Detailed Breakdown (if data supports it)
   Example: "This breaks down into $800,000 from operating revenue and $434,567 from other sources..."

3. Key Insights (2-3 bullet points)
   Example:
   • Revenue is concentrated in the top 5 accounts
   • Growth trend shows 15% increase year-over-year
   • [Data source] accounts for 60% of total revenue

4. Recommendations or Follow-ups (optional, 1-2 sentences)
   Example: "Would you like to see a breakdown by time period or compare this to expenses?"

FORMATTING GUIDELINES:
- Use professional financial language
- Be specific and data-driven
- Reference the SQL query if it helps explain the analysis
- Use bullet points for insights
- Keep paragraphs short and readable
- End with helpful suggestions

CRITICAL - CONTEXT SUMMARY FOR CONVERSATION HISTORY:
After your response, add a special section for conversation history.
Format it EXACTLY like this (on a new line after your response):

---CONTEXT_SUMMARY---
[Create a HIGHLY DENSE, SHORT summary (30-50 words) that captures:]
- What user asked about (include specific terms they used)
- Key context: Data source, Time period (Month Year format), Account types
- Main result with actual number/value
- Any important qualifiers (loss vs profit, highest/lowest, etc.)

CONTEXT SUMMARY EXAMPLES:

Example 1 (Basic Query):
User asked about total revenue from [data source] for [time period]. Found $3,369,378.43 from [data source] for [time period].

Example 2 (Follow-up Context):
User asked "net profit for the above period and report" (referring to [data source], [time period] from previous query). Calculated net profit of $386,365.91 from [data source] for [time period].

Example 3 (Multi-query Context Chain):
User asked for account breakdown "for that period" ([data source], [time period] context from 2 queries ago). Returned 8 accounts with [top account] highest at $3.37M.

Example 4 (Comparison):
User asked to compare [period A] vs [period B] performance. Found [period A] had loss of -$727,079 while [period B] had profit of $1,111,586.

Example 5 (Year-over-Year):
User asked which expense category had highest increase this year. Found [expense category] increased by $1,950,422 from [previous year] ($48.05M) to [current year] ($50.00M).

YOUR RESPONSE FORMAT:
[Your full professional response here]

---CONTEXT_SUMMARY---
[Your dense 30-50 word context summary here]

Generate the response now:"""

# =============================================================================
# TEMPLATE UTILITIES
# =============================================================================


def format_financial_data(data_summary: dict) -> str:
    """Format financial data using the data summary template"""
    return DATA_SUMMARY_TEMPLATE.format(**data_summary)


def format_account_details(account_type: str, accounts: list) -> str:
    """Format account details using the account template"""
    total_value = sum(acc.get("value", 0) for acc in accounts)
    record_count = len(accounts)
    avg_value = total_value / record_count if record_count > 0 else 0

    top_accounts = "\n".join(
        [
            f"  - {acc.get('account_name', 'Unknown')}: ${acc.get('value', 0):,.2f}"
            for acc in sorted(accounts, key=lambda x: x.get("value", 0), reverse=True)[
                :3
            ]
        ]
    )

    return ACCOUNT_DETAILS_TEMPLATE.format(
        account_type=account_type.replace("_", " ").title(),
        total_value=total_value,
        record_count=record_count,
        avg_value=avg_value,
        top_accounts=top_accounts,
    )


def get_error_template(error_type: str) -> dict:
    """Get error response template by type"""
    return ERROR_RESPONSE_TEMPLATES.get(error_type, {})


def calculate_confidence_score(
    data_quality: float, pattern_clarity: float, data_completeness: float
) -> float:
    """Calculate confidence score based on multiple factors"""
    return min(0.95, max(0.1, (data_quality + pattern_clarity + data_completeness) / 3))


# =============================================================================
# STRUCTURED LLM RESPONSE TEMPLATES
# =============================================================================

STRUCTURED_RESPONSE_PROMPT = """
You must respond in the following JSON structure for ALL queries:

{
    "summary": "Brief 1-2 sentence summary of the key points and findings",
    "response": "Detailed response with specific data, insights, and recommendations"
}

Guidelines:
1. Summary should be concise and capture the essence of the response
2. Response should be comprehensive with specific numbers, percentages, and actionable insights
3. Always include specific data points when available
4. Provide clear recommendations when appropriate
5. Use professional financial language
6. Ensure both fields are always present and non-empty

Example:
{
    "summary": "Revenue increased 15% to $2.3M with strong growth in Q4. Operating expenses rose 8% to $1.8M.",
    "response": "Based on the financial data analysis:\n\n**Revenue Performance:**\n- Total revenue: $2,300,000 (15% increase from previous period)\n- Q4 showed strongest growth at 22% increase\n- Top performing accounts: Product Sales ($1.2M), Services ($800K)\n\n**Expense Analysis:**\n- Operating expenses: $1,800,000 (8% increase)\n- Cost of goods sold: $920,000 (12% increase)\n- Administrative costs: $450,000 (5% increase)\n\n**Key Insights:**\n- Profit margin improved to 21.7% (up from 19.2%)\n- Revenue growth outpaced expense growth\n- Strong operational efficiency maintained\n\n**Recommendations:**\n1. Continue current growth strategies\n2. Monitor COGS increases closely\n3. Consider expanding high-performing service lines"
}
"""

INTENT_ANALYSIS_WITH_HISTORY_PROMPT = """
Analyze the following query and conversation history to determine intent and extract parameters.

IMPORTANT: You must include a "should_fire_api" field in your response.
Set "should_fire_api": true if the query requires financial data retrieval.
Set "should_fire_api": false if the query is conversational or doesn't need data.

User Query: "{query}"

Conversation History:
{conversation_summaries}

Available APIs:
{api_info}

Instructions:
1. Analyze the query intent and determine if financial data is needed
2. If data is needed, construct appropriate API parameters
3. Include "should_fire_api": true/false in your JSON response
4. If should_fire_api is true, provide complete API parameters
5. If should_fire_api is false, provide reasoning for conversational response

Determine:
1. Intent type (data_retrieval, analysis, comparison, trend, summary, etc.)
2. If intent is data_retrieval, extract specific filters and parameters
3. Time period requirements
4. Account types or categories needed
5. Aggregation level required
6. Whether conversation history provides relevant context

Respond in this JSON structure:
{
    "intent": "data_retrieval|analysis|comparison|trend|summary|other",
    "is_data_retrieval": true/false,
    "should_fire_api": true/false,
    "api_params": {
        "account_types": ["revenue", "expense", "cogs", "tax"],
        "time_period": "2024-01-01 to 2024-12-31",
        "aggregation_level": "monthly|quarterly|yearly",
        "filters": {
            "account_names": ["specific accounts if mentioned"],
            "min_value": 1000,
            "max_value": 100000
        }
    },
    "confidence": 0.85,
    "reasoning": "Explanation of intent determination and parameter extraction"
}

Focus on:
- Clear intent classification
- Accurate parameter extraction for data retrieval
- Consideration of conversation context
- Confidence scoring based on query clarity
- Proper should_fire_api determination
"""

CONVERSATION_SUMMARY_PROMPT = """
Create a concise summary of this conversation interaction:

User Query: "{query}"
LLM Response: "{response}"

Create a summary that captures:
1. The main topic/question
2. Key findings or data points mentioned
3. Any specific requests or requirements
4. Important context for future interactions

Keep the summary to 1-2 sentences maximum. Focus on the most important information that would be useful for future context.

Example format: "User asked about Q4 revenue trends. Found 15% growth to $2.3M with strongest performance in December ($800K)."
"""

# =============================================================================
# TEMPLATE VALIDATION
# =============================================================================


def validate_template(template: str, required_fields: list) -> bool:
    """Validate that template contains all required fields"""
    for field in required_fields:
        if f"{{{field}}}" not in template:
            return False
    return True


# Template validation for key templates
TEMPLATE_VALIDATION = {
    "DATA_SUMMARY_TEMPLATE": validate_template(
        DATA_SUMMARY_TEMPLATE,
        [
            "total_revenue",
            "revenue_count",
            "avg_revenue",
            "top_revenue_accounts",
            "total_expenses",
            "expense_count",
            "avg_expense",
            "top_expense_accounts",
            "net_profit",
            "profit_margin",
            "revenue_expense_ratio",
            "total_records",
            "zero_value_count",
            "completeness",
        ],
    ),
    "ACCOUNT_DETAILS_TEMPLATE": validate_template(
        ACCOUNT_DETAILS_TEMPLATE,
        ["account_type", "total_value", "record_count", "avg_value", "top_accounts"],
    ),
}
