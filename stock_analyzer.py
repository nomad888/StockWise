"""
Main Stock Analyzer - Orchestrates all analysis modules
"""
from utils.data_fetcher import DataFetcher
from utils.scorer import Scorer
from analyzers.fundamental import FundamentalAnalyzer
from analyzers.valuation import ValuationAnalyzer
from analyzers.dividend import DividendAnalyzer
from analyzers.technical import TechnicalAnalyzer
from analyzers.sentiment import SentimentAnalyzer
from typing import Dict, List, Any

class StockAnalyzer:
    """Main class that orchestrates all stock analysis"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol.upper()
        self.data_fetcher = DataFetcher(symbol)
        self.scorer = Scorer()
        
        # Initialize all analyzers
        self.fundamental = FundamentalAnalyzer(self.data_fetcher)
        self.valuation = ValuationAnalyzer(self.data_fetcher)
        self.dividend = DividendAnalyzer(self.data_fetcher)
        self.technical = TechnicalAnalyzer(self.data_fetcher)
        self.sentiment = SentimentAnalyzer(self.data_fetcher)
        
        self.all_results = []
    
    def run_analysis(self) -> Dict[str, Any]:
        """
        Run complete analysis covering all 20 questions
        Returns: Dictionary containing all analysis results and recommendation
        """
        print(f"\n{'='*80}")
        print(f"Starting comprehensive analysis for {self.symbol}...")
        print(f"{'='*80}\n")
        
        # Run all analyses
        print("📊 Running Fundamental Analysis (Questions 1-6)...")
        fundamental_results = self.fundamental.get_all_analyses()
        self._process_results(fundamental_results, 'fundamental')
        
        print("💰 Running Valuation Analysis (Questions 7-10)...")
        valuation_results = self.valuation.get_all_analyses()
        self._process_results(valuation_results, 'valuation')
        
        print("💵 Running Dividend Analysis (Question 11)...")
        dividend_results = self.dividend.get_all_analyses()
        self._process_results(dividend_results, 'dividend')
        
        print("📈 Running Technical Analysis (Questions 12-16)...")
        technical_results = self.technical.get_all_analyses()
        self._process_results(technical_results, 'technical')
        
        print("📰 Running Sentiment Analysis (Questions 17-20)...")
        sentiment_results = self.sentiment.get_all_analyses()
        self._process_results(sentiment_results, 'sentiment')
        
        print("\n✅ Analysis complete!\n")
        
        # Get final scoring summary
        summary = self.scorer.get_summary()
        
        return {
            'symbol': self.symbol,
            'company_name': self.data_fetcher.get_stock_info().get('longName', self.symbol),
            'results': self.all_results,
            'summary': summary
        }
    
    def _process_results(self, results: List[Dict], category: str):
        """Process results from an analyzer and add to scorer"""
        for result in results:
            self.all_results.append(result)
            
            # Add score if available
            if 'score' in result:
                score = result['score']
                question = result.get('question_en', '')
                self.scorer.add_score(category, score, question)
    
    def get_stock_info(self) -> Dict[str, Any]:
        """Get basic stock information"""
        return self.data_fetcher.get_stock_info()
