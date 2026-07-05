"""
Pydantic models for API request/response validation
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class AnalysisRequest(BaseModel):
    """Request model for stock analysis"""
    symbol: str = Field(..., description="Stock symbol to analyze (e.g., AAPL, MSFT)", min_length=1, max_length=10)
    
    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL"
            }
        }

class QuestionAnswer(BaseModel):
    """Model for individual question and answer"""
    question_en: str = Field(..., description="Question in English")
    question_zh: str = Field(..., description="Question in Chinese")
    answer: Dict[str, Any] = Field(..., description="Answer details")
    score: Optional[float] = Field(None, description="Score for this question (0-100)")

class CategoryScore(BaseModel):
    """Model for category score breakdown"""
    fundamental: float = Field(..., description="Fundamental analysis score")
    valuation: float = Field(..., description="Valuation analysis score")
    dividend: float = Field(..., description="Dividend analysis score")
    technical: float = Field(..., description="Technical analysis score")
    sentiment: float = Field(..., description="Sentiment analysis score")

class ScoreSummary(BaseModel):
    """Model for scoring summary"""
    overall_score: float = Field(..., description="Overall weighted score (0-100)")
    recommendation_en: str = Field(..., description="Recommendation in English")
    recommendation_zh: str = Field(..., description="Recommendation in Chinese")
    confidence: str = Field(..., description="Confidence level")
    category_scores: CategoryScore = Field(..., description="Breakdown by category")

class AnalysisResponse(BaseModel):
    """Response model for stock analysis"""
    symbol: str = Field(..., description="Stock symbol analyzed")
    company_name: str = Field(..., description="Company name")
    timestamp: str = Field(..., description="Analysis timestamp")
    summary: ScoreSummary = Field(..., description="Analysis summary and recommendation")
    results: List[QuestionAnswer] = Field(..., description="Detailed Q&A results for all 20 questions")
    
    class Config:
        json_schema_extra = {
            "example": {
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
                "results": []
            }
        }

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid stock symbol",
                "detail": "Symbol 'INVALID' not found"
            }
        }

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0"
            }
        }
