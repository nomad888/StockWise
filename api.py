"""
FastAPI Web Application for StockWise Analysis
Provides RESTful API endpoints for stock analysis
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime
import traceback
from typing import Dict, Any

from models.api_models import (
    AnalysisRequest,
    AnalysisResponse,
    ErrorResponse,
    HealthResponse,
    QuestionAnswer,
    ScoreSummary,
    CategoryScore
)
from stock_analyzer import StockAnalyzer

# Create FastAPI app
app = FastAPI(
    title="StockWise API",
    description="Comprehensive Stock Analysis API - Analyzes stocks based on 20 critical questions covering fundamental, valuation, technical, and sentiment analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception:
    pass  # Static directory might not exist yet

@app.get("/", response_class=HTMLResponse, tags=["Root"])
async def root():
    """
    Root endpoint - Returns API information
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>StockWise API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 10px;
                backdrop-filter: blur(10px);
            }
            h1 { margin-top: 0; }
            a {
                color: #ffd700;
                text-decoration: none;
                font-weight: bold;
            }
            a:hover { text-decoration: underline; }
            .endpoint {
                background: rgba(0, 0, 0, 0.2);
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
            }
            code {
                background: rgba(0, 0, 0, 0.3);
                padding: 2px 6px;
                border-radius: 3px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 StockWise API</h1>
            <p>Comprehensive Stock Analysis API based on 20 critical questions</p>
            
            <h2>🚀 Quick Start</h2>
            <div class="endpoint">
                <strong>Analyze a Stock:</strong><br>
                <code>POST /api/analyze</code><br>
                Body: <code>{"symbol": "AAPL"}</code>
            </div>
            
            <h2>📚 Documentation</h2>
            <ul>
                <li><a href="/docs">Interactive API Docs (Swagger UI)</a></li>
                <li><a href="/redoc">Alternative Docs (ReDoc)</a></li>
                <li><a href="/api/health">Health Check</a></li>
            </ul>
            
            <h2>🔍 Analysis Coverage</h2>
            <ul>
                <li><strong>Fundamental Analysis</strong> (Q1-Q6): Business model, profitability, growth, balance sheet, cash flow, management</li>
                <li><strong>Valuation Analysis</strong> (Q7-Q10): P/E, P/B ratios, historical valuation, peer comparison</li>
                <li><strong>Dividend Analysis</strong> (Q11): Dividend yield and sustainability</li>
                <li><strong>Technical Analysis</strong> (Q12-Q16): Trends, indicators (MACD, RSI, KDJ), patterns, moving averages, volume</li>
                <li><strong>Sentiment Analysis</strong> (Q17-Q20): News, analyst ratings, social sentiment, risk events</li>
            </ul>
            
            <h2>💡 Example Usage</h2>
            <div class="endpoint">
                <strong>cURL:</strong><br>
                <code>curl -X POST http://localhost:8000/api/analyze -H "Content-Type: application/json" -d '{"symbol": "AAPL"}'</code>
            </div>
            
            <p style="margin-top: 30px; text-align: center; opacity: 0.8;">
                Built with FastAPI • Powered by yfinance
            </p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    Returns the status and version of the API
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0"
    )

@app.post(
    "/api/analyze",
    response_model=AnalysisResponse,
    responses={
        200: {"description": "Successful analysis"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    tags=["Analysis"]
)
async def analyze_stock(request: AnalysisRequest):
    """
    Analyze a stock based on 20 comprehensive questions
    
    This endpoint performs a complete stock analysis covering:
    - Fundamental analysis (6 questions)
    - Valuation analysis (4 questions)
    - Dividend analysis (1 question)
    - Technical analysis (5 questions)
    - Sentiment analysis (4 questions)
    
    Returns a detailed analysis with scores and buy/sell recommendation.
    """
    try:
        # Validate and clean symbol
        symbol = request.symbol.strip().upper()
        
        if not symbol:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock symbol cannot be empty"
            )
        
        # Create analyzer and run analysis
        print(f"Analyzing stock: {symbol}")
        analyzer = StockAnalyzer(symbol)
        results = analyzer.run_analysis()
        
        # Convert results to API response format
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Build question-answer list
        qa_list = []
        for result in results['results']:
            qa = QuestionAnswer(
                question_en=result.get('question_en', ''),
                question_zh=result.get('question_zh', ''),
                answer=result.get('answer', {}),
                score=result.get('score')
            )
            qa_list.append(qa)
        
        # Build summary
        summary_data = results['summary']
        category_scores = CategoryScore(
            fundamental=summary_data['category_scores']['fundamental'],
            valuation=summary_data['category_scores']['valuation'],
            dividend=summary_data['category_scores']['dividend'],
            technical=summary_data['category_scores']['technical'],
            sentiment=summary_data['category_scores']['sentiment']
        )
        
        summary = ScoreSummary(
            overall_score=summary_data['overall_score'],
            recommendation_en=summary_data['recommendation_en'],
            recommendation_zh=summary_data['recommendation_zh'],
            confidence=summary_data['confidence'],
            category_scores=category_scores
        )
        
        # Build response
        response = AnalysisResponse(
            symbol=results['symbol'],
            company_name=results['company_name'],
            timestamp=timestamp,
            summary=summary,
            results=qa_list
        )
        
        print(f"Analysis complete for {symbol}: {summary.recommendation_en}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        error_detail = str(e)
        print(f"Error analyzing {request.symbol}: {error_detail}")
        traceback.print_exc()
        
        # Check if it's a symbol not found error
        if "No data found" in error_detail or "No timezone found" in error_detail:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Stock symbol '{request.symbol}' not found or invalid"
            )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing stock: {error_detail}"
        )

@app.get(
    "/api/analyze/{symbol}",
    response_model=AnalysisResponse,
    responses={
        200: {"description": "Successful analysis"},
        404: {"model": ErrorResponse, "description": "Stock not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    tags=["Analysis"]
)
async def analyze_stock_get(symbol: str):
    """
    Analyze a stock using GET request (alternative to POST)
    
    This is a convenience endpoint that accepts the stock symbol as a path parameter.
    """
    request = AnalysisRequest(symbol=symbol)
    return await analyze_stock(request)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "detail": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    print("Starting StockWise API server...")
    print("API Documentation: http://localhost:8000/docs")
    print("Alternative Docs: http://localhost:8000/redoc")
    print("Web Interface: http://localhost:8000/static/index.html")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
