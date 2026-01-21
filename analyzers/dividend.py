"""
Dividend Analysis Module (Question 11)
"""
from typing import Dict, Any, List
import pandas as pd

class DividendAnalyzer:
    """Analyze dividend metrics of a stock"""
    
    def __init__(self, data_fetcher):
        self.fetcher = data_fetcher
        self.info = data_fetcher.get_stock_info()
        self.dividends = data_fetcher.get_dividends()
    
    def analyze_dividend(self) -> Dict[str, Any]:
        """
        Q11: 这只股票有没有分红？股息率高不高？
        Does this stock pay dividends? Is the dividend yield high?
        """
        dividend_yield = self.info.get('dividendYield', 0) * 100 if self.info.get('dividendYield') else 0
        dividend_rate = self.info.get('dividendRate', 0)
        payout_ratio = self.info.get('payoutRatio', 0) * 100 if self.info.get('payoutRatio') else 0
        five_year_avg_yield = self.info.get('fiveYearAvgDividendYield', 0)
        
        score = 50
        assessment = "No dividend"
        
        # Check if company pays dividends
        if dividend_yield > 0 or dividend_rate > 0:
            if dividend_yield > 4:
                score = 85
                assessment = "High dividend yield - Attractive for income investors"
            elif dividend_yield > 2:
                score = 70
                assessment = "Good dividend yield"
            elif dividend_yield > 0:
                score = 55
                assessment = "Low dividend yield"
            
            # Adjust for payout ratio sustainability
            if payout_ratio > 0:
                if payout_ratio > 80:
                    score = max(0, score - 15)
                    assessment += " (high payout ratio - sustainability concern)"
                elif payout_ratio < 60:
                    score = min(100, score + 10)
                    assessment += " (sustainable payout ratio)"
        else:
            score = 45
            assessment = "No dividend - Growth-focused company"
        
        # Analyze dividend history
        dividend_history = "N/A"
        if self.dividends is not None and len(self.dividends) > 0:
            recent_dividends = self.dividends.tail(5)
            if len(recent_dividends) >= 2:
                trend = "increasing" if recent_dividends.iloc[-1] > recent_dividends.iloc[0] else "stable/decreasing"
                dividend_history = f"{len(self.dividends)} payments on record, {trend} trend"
                
                if trend == "increasing":
                    score = min(100, score + 5)
        
        return {
            'question_en': 'Does this stock pay dividends? Is the dividend yield high?',
            'question_zh': '这只股票有没有分红？股息率高不高？',
            'answer': {
                'dividend_yield': f"{dividend_yield:.2f}%",
                'dividend_rate': f"${dividend_rate:.2f}" if dividend_rate else "N/A",
                'payout_ratio': f"{payout_ratio:.2f}%" if payout_ratio else "N/A",
                'five_year_avg_yield': f"{five_year_avg_yield:.2f}%" if five_year_avg_yield else "N/A",
                'dividend_history': dividend_history,
                'assessment': assessment
            },
            'score': score
        }
    
    def get_all_analyses(self) -> List[Dict]:
        """Get all dividend analyses"""
        return [self.analyze_dividend()]
