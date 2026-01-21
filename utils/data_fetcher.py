"""
Data fetching utilities for stock information
"""
import yfinance as yf
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import json
import os

class DataFetcher:
    """Centralized data fetching with caching support"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol.upper()
        self.ticker = yf.Ticker(self.symbol)
        self._cache = {}
        
    def get_stock_info(self) -> Dict[str, Any]:
        """Get basic stock information"""
        if 'info' not in self._cache:
            try:
                self._cache['info'] = self.ticker.info
            except Exception as e:
                print(f"Error fetching stock info: {e}")
                self._cache['info'] = {}
        return self._cache['info']
    
    def get_historical_data(self, period: str = "1y") -> Any:
        """Get historical price data"""
        cache_key = f'history_{period}'
        if cache_key not in self._cache:
            try:
                self._cache[cache_key] = self.ticker.history(period=period)
            except Exception as e:
                print(f"Error fetching historical data: {e}")
                self._cache[cache_key] = None
        return self._cache[cache_key]
    
    def get_financials(self) -> Dict[str, Any]:
        """Get financial statements"""
        if 'financials' not in self._cache:
            try:
                self._cache['financials'] = {
                    'income_stmt': self.ticker.income_stmt,
                    'balance_sheet': self.ticker.balance_sheet,
                    'cash_flow': self.ticker.cashflow,
                    'quarterly_income': self.ticker.quarterly_income_stmt,
                    'quarterly_balance': self.ticker.quarterly_balance_sheet,
                    'quarterly_cashflow': self.ticker.quarterly_cashflow
                }
            except Exception as e:
                print(f"Error fetching financials: {e}")
                self._cache['financials'] = {}
        return self._cache['financials']
    
    def get_dividends(self) -> Any:
        """Get dividend history"""
        if 'dividends' not in self._cache:
            try:
                self._cache['dividends'] = self.ticker.dividends
            except Exception as e:
                print(f"Error fetching dividends: {e}")
                self._cache['dividends'] = None
        return self._cache['dividends']
    
    def get_recommendations(self) -> Any:
        """Get analyst recommendations"""
        if 'recommendations' not in self._cache:
            try:
                self._cache['recommendations'] = self.ticker.recommendations
            except Exception as e:
                print(f"Error fetching recommendations: {e}")
                self._cache['recommendations'] = None
        return self._cache['recommendations']
    
    def get_news(self, limit: int = 10) -> list:
        """Get recent news about the stock"""
        if 'news' not in self._cache:
            try:
                self._cache['news'] = self.ticker.news[:limit] if self.ticker.news else []
            except Exception as e:
                print(f"Error fetching news: {e}")
                self._cache['news'] = []
        return self._cache['news']
    
    def get_major_holders(self) -> Any:
        """Get major shareholders information"""
        if 'holders' not in self._cache:
            try:
                self._cache['holders'] = {
                    'major_holders': self.ticker.major_holders,
                    'institutional_holders': self.ticker.institutional_holders,
                    'mutualfund_holders': self.ticker.mutualfund_holders
                }
            except Exception as e:
                print(f"Error fetching holders: {e}")
                self._cache['holders'] = {}
        return self._cache['holders']
    
    def get_earnings(self) -> Any:
        """Get earnings data"""
        if 'earnings' not in self._cache:
            try:
                self._cache['earnings'] = {
                    'earnings': self.ticker.earnings,
                    'quarterly_earnings': self.ticker.quarterly_earnings
                }
            except Exception as e:
                print(f"Error fetching earnings: {e}")
                self._cache['earnings'] = {}
        return self._cache['earnings']
    
    def clear_cache(self):
        """Clear the data cache"""
        self._cache = {}
