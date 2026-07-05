# StockWise API Documentation

## Overview

The StockWise API provides comprehensive stock analysis based on 20 critical questions covering fundamental, valuation, technical, and sentiment analysis. The API returns detailed analysis results with buy/sell recommendations in both English and Chinese.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. The API is open for testing purposes.

## Endpoints

### 1. Health Check

Check if the API is running and healthy.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

**Example:**
```bash
curl http://localhost:8000/api/health
```

---

### 2. Analyze Stock (POST)

Perform comprehensive analysis on a stock symbol.

**Endpoint:** `POST /api/analyze`

**Request Body:**
```json
{
  "symbol": "AAPL"
}
```

**Parameters:**
- `symbol` (string, required): Stock ticker symbol (e.g., AAPL, MSFT, TSLA)

**Response:** `200 OK`
```json
{
  "symbol": "AAPL",
  "company_name": "Apple Inc.",
  "timestamp": "2026-01-21 11:00:00",
  "summary": {
    "overall_score": 54.24,
    "recommendation_en": "Hold",
    "recommendation_zh": "持有",
    "confidence": "Medium",
    "category_scores": {
      "fundamental": 61.0,
      "valuation": 46.2,
      "dividend": 100.0,
      "technical": 43.0,
      "sentiment": 57.5
    }
  },
  "results": [
    {
      "question_en": "What does this company do?",
      "question_zh": "这家公司主要是做什么的？",
      "answer": {
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "business_summary": "..."
      },
      "score": null
    }
    // ... 19 more questions
  ]
}
```

**Error Responses:**

`400 Bad Request` - Invalid request
```json
{
  "error": "Invalid request",
  "detail": "Stock symbol cannot be empty"
}
```

`404 Not Found` - Stock symbol not found
```json
{
  "error": "Stock not found",
  "detail": "Stock symbol 'INVALID' not found or invalid"
}
```

`500 Internal Server Error` - Server error
```json
{
  "error": "Internal server error",
  "detail": "Error details..."
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL"}'
```

**Python Example:**
```python
import requests

response = requests.post(
    'http://localhost:8000/api/analyze',
    json={'symbol': 'AAPL'}
)

data = response.json()
print(f"Overall Score: {data['summary']['overall_score']}")
print(f"Recommendation: {data['summary']['recommendation_en']}")
```

**JavaScript Example:**
```javascript
fetch('http://localhost:8000/api/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ symbol: 'AAPL' })
})
.then(response => response.json())
.then(data => {
  console.log('Overall Score:', data.summary.overall_score);
  console.log('Recommendation:', data.summary.recommendation_en);
});
```

---

### 3. Analyze Stock (GET)

Alternative endpoint using GET request with symbol as path parameter.

**Endpoint:** `GET /api/analyze/{symbol}`

**Parameters:**
- `symbol` (string, path parameter): Stock ticker symbol

**Response:** Same as POST endpoint

**Example:**
```bash
curl http://localhost:8000/api/analyze/AAPL
```

---

## Response Schema

### AnalysisResponse

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | Stock symbol analyzed |
| `company_name` | string | Full company name |
| `timestamp` | string | Analysis timestamp |
| `summary` | ScoreSummary | Analysis summary and recommendation |
| `results` | QuestionAnswer[] | Array of 20 Q&A results |

### ScoreSummary

| Field | Type | Description |
|-------|------|-------------|
| `overall_score` | float | Overall weighted score (0-100) |
| `recommendation_en` | string | Recommendation in English |
| `recommendation_zh` | string | Recommendation in Chinese |
| `confidence` | string | Confidence level (High/Medium/Low) |
| `category_scores` | CategoryScore | Score breakdown by category |

### CategoryScore

| Field | Type | Description |
|-------|------|-------------|
| `fundamental` | float | Fundamental analysis score (0-100) |
| `valuation` | float | Valuation analysis score (0-100) |
| `dividend` | float | Dividend analysis score (0-100) |
| `technical` | float | Technical analysis score (0-100) |
| `sentiment` | float | Sentiment analysis score (0-100) |

### QuestionAnswer

| Field | Type | Description |
|-------|------|-------------|
| `question_en` | string | Question in English |
| `question_zh` | string | Question in Chinese |
| `answer` | object | Answer details (varies by question) |
| `score` | float \| null | Individual question score (0-100) |

---

## The 20 Questions

### Fundamental Analysis (Q1-Q6)
1. Business model and core products
2. Profitability metrics
3. Revenue growth
4. Balance sheet health
5. Cash flow analysis
6. Management and shareholders

### Valuation Analysis (Q7-Q10)
7. P/E and P/B ratios vs industry
8. Historical valuation positioning
9. P/S, P/CF peer comparison
10. Earnings forecast alignment

### Dividend Analysis (Q11)
11. Dividend yield and sustainability

### Technical Analysis (Q12-Q16)
12. Price trend
13. Technical indicators (MACD, RSI, KDJ)
14. Chart patterns
15. Moving average positioning
16. Volume analysis

### Sentiment Analysis (Q17-Q20)
17. Recent news
18. Analyst ratings
19. Social sentiment
20. Risk events

---

## Recommendation Thresholds

| Score Range | Recommendation |
|-------------|----------------|
| 75-100 | Strong Buy (强烈买入) |
| 60-74 | Buy (买入) |
| 40-59 | Hold (持有) |
| 25-39 | Sell (卖出) |
| 0-24 | Strong Sell (强烈卖出) |

---

## Interactive Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These interfaces allow you to:
- View all endpoints
- See request/response schemas
- Test API calls directly in the browser
- Download OpenAPI specification

---

## Rate Limiting

Currently, there are no rate limits. For production deployment, consider implementing rate limiting to prevent abuse.

---

## CORS

The API has CORS enabled for all origins (`*`) to allow frontend integration. In production, configure specific allowed origins.

---

## Error Handling

All errors follow a consistent format:

```json
{
  "error": "Error type",
  "detail": "Detailed error message"
}
```

Common HTTP status codes:
- `200` - Success
- `400` - Bad Request (invalid input)
- `404` - Not Found (invalid stock symbol)
- `500` - Internal Server Error

---

## Running the API

### Start the server:
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Start the server
uvicorn api:app --reload

# Or run directly
python api.py
```

The API will be available at http://localhost:8000

### Web Interface

Access the web interface at http://localhost:8000/static/index.html

---

## Data Sources

- **Stock Data:** Yahoo Finance (via yfinance)
- **Financial Statements:** Yahoo Finance
- **News:** Yahoo Finance News
- **Analyst Ratings:** Yahoo Finance
- **Technical Indicators:** Calculated using ta library

---

## Limitations

1. Data is sourced from free Yahoo Finance API (may have delays)
2. Optimized for US stocks (NYSE, NASDAQ)
3. Social sentiment analysis is limited without premium APIs
4. Pattern detection is basic

---

## Support

For issues or questions:
- Check the interactive docs at `/docs`
- Review this documentation
- Test with known symbols (AAPL, MSFT, GOOGL)

---

## Version History

**v1.0.0** (2026-01-21)
- Initial release
- POST and GET endpoints for stock analysis
- 20-question comprehensive analysis
- Bilingual support (English/Chinese)
- Interactive web interface
