"""
Configuration settings for Stock Analysis Application
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
ALPHA_VANTAGE_KEY = os.getenv('ALPHA_VANTAGE_KEY', '')

# Scoring Weights (total should be 100)
WEIGHTS = {
    'fundamental': 30,    # Questions 1-6
    'valuation': 25,      # Questions 7-10
    'dividend': 5,        # Question 11
    'technical': 25,      # Questions 12-16
    'sentiment': 15       # Questions 17-20
}

# Buy/Sell Thresholds (0-100 scale)
THRESHOLDS = {
    'strong_buy': 75,
    'buy': 60,
    'hold': 40,
    'sell': 25,
    'strong_sell': 0
}

# Technical Analysis Parameters
TECHNICAL_PARAMS = {
    'rsi_overbought': 70,
    'rsi_oversold': 30,
    'ma_short': 50,      # 50-day moving average
    'ma_long': 200,      # 200-day moving average
}

# Valuation Parameters
VALUATION_PARAMS = {
    'pe_high': 30,       # High P/E threshold
    'pe_low': 15,        # Low P/E threshold
    'pb_high': 5,        # High P/B threshold
    'pb_low': 1,         # Low P/B threshold
}

# Language Settings
DEFAULT_LANGUAGE = 'bilingual'  # Options: 'en', 'zh', 'bilingual'

# Report Settings
REPORT_FORMAT = 'markdown'  # Options: 'text', 'markdown', 'html'
INCLUDE_CHARTS = False      # Set to True if you want to generate charts

# Cache Settings
CACHE_ENABLED = True
CACHE_DURATION_HOURS = 1
