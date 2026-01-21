"""
Valuation Analysis Module (Questions 7-10)
"""
from typing import Dict, Any, List
import pandas as pd
import numpy as np
import config

class ValuationAnalyzer:
    """Analyze valuation metrics of a stock"""
    
    def __init__(self, data_fetcher):
        self.fetcher = data_fetcher
        self.info = data_fetcher.get_stock_info()
    
    def analyze_pe_pb_ratios(self) -> Dict[str, Any]:
        """
        Q7: 这只股票的市盈率、市净率相比行业平均如何？
        How do P/E and P/B ratios compare to industry average?
        """
        pe_ratio = self.info.get('trailingPE', 0)
        pb_ratio = self.info.get('priceToBook', 0)
        forward_pe = self.info.get('forwardPE', 0)
        
        # Industry averages (approximate - would need external data for exact values)
        sector = self.info.get('sector', 'Unknown')
        
        score = 50
        assessment = "Fair valuation"
        
        # Score based on P/E ratio
        if pe_ratio > 0:
            if pe_ratio < 15:
                score = 80
                assessment = "Undervalued based on P/E"
            elif pe_ratio < 25:
                score = 60
                assessment = "Fairly valued"
            elif pe_ratio < 40:
                score = 40
                assessment = "Moderately overvalued"
            else:
                score = 25
                assessment = "Highly overvalued"
        
        # Adjust for P/B ratio
        if pb_ratio > 0:
            if pb_ratio < 1:
                score = min(100, score + 15)
            elif pb_ratio > 5:
                score = max(0, score - 10)
        
        return {
            'question_en': 'How do P/E and P/B ratios compare to industry average?',
            'question_zh': '这只股票的市盈率、市净率相比行业平均如何？',
            'answer': {
                'pe_ratio': f"{pe_ratio:.2f}" if pe_ratio else "N/A",
                'pb_ratio': f"{pb_ratio:.2f}" if pb_ratio else "N/A",
                'forward_pe': f"{forward_pe:.2f}" if forward_pe else "N/A",
                'sector': sector,
                'assessment': assessment
            },
            'score': score
        }
    
    def analyze_historical_valuation(self) -> Dict[str, Any]:
        """
        Q8: 现在是历史高估还是低估阶段？估值在历史区间哪一档？
        Is it historically overvalued or undervalued? Where in historical range?
        """
        current_price = self.info.get('currentPrice', 0)
        fifty_two_week_high = self.info.get('fiftyTwoWeekHigh', 0)
        fifty_two_week_low = self.info.get('fiftyTwoWeekLow', 0)
        
        score = 50
        position = "Mid-range"
        
        if fifty_two_week_high > 0 and fifty_two_week_low > 0 and current_price > 0:
            # Calculate position in 52-week range
            range_span = fifty_two_week_high - fifty_two_week_low
            position_pct = ((current_price - fifty_two_week_low) / range_span * 100) if range_span > 0 else 50
            
            if position_pct < 25:
                score = 85
                position = f"Near 52-week low ({position_pct:.1f}% of range) - Potentially undervalued"
            elif position_pct < 50:
                score = 65
                position = f"Below mid-range ({position_pct:.1f}% of range) - Fair value"
            elif position_pct < 75:
                score = 45
                position = f"Above mid-range ({position_pct:.1f}% of range) - Elevated"
            else:
                score = 25
                position = f"Near 52-week high ({position_pct:.1f}% of range) - Potentially overvalued"
        
        return {
            'question_en': 'Is it historically overvalued or undervalued? Where in historical range?',
            'question_zh': '现在是历史高估还是低估阶段？估值在历史区间哪一档？',
            'answer': {
                'current_price': f"${current_price:.2f}",
                '52_week_high': f"${fifty_two_week_high:.2f}",
                '52_week_low': f"${fifty_two_week_low:.2f}",
                'position': position
            },
            'score': score
        }
    
    def analyze_peer_valuation(self) -> Dict[str, Any]:
        """
        Q9: 市销率、市现率等估值指标在同行中排第几？
        How do P/S, P/CF ratios rank among peers?
        """
        ps_ratio = self.info.get('priceToSalesTrailing12Months', 0)
        peg_ratio = self.info.get('pegRatio', 0)
        enterprise_value = self.info.get('enterpriseValue', 0)
        ebitda = self.info.get('ebitda', 0)
        
        ev_ebitda = (enterprise_value / ebitda) if ebitda and ebitda > 0 else 0
        
        score = 50
        assessment = "Average valuation metrics"
        
        # Score based on P/S ratio
        if ps_ratio > 0:
            if ps_ratio < 2:
                score = 75
                assessment = "Attractive P/S ratio"
            elif ps_ratio < 5:
                score = 55
                assessment = "Moderate P/S ratio"
            else:
                score = 35
                assessment = "High P/S ratio"
        
        # Adjust for PEG ratio (P/E to growth)
        if peg_ratio > 0:
            if peg_ratio < 1:
                score = min(100, score + 15)
            elif peg_ratio > 2:
                score = max(0, score - 10)
        
        return {
            'question_en': 'How do P/S, P/CF ratios rank among peers?',
            'question_zh': '市销率、市现率等估值指标在同行中排第几？',
            'answer': {
                'ps_ratio': f"{ps_ratio:.2f}" if ps_ratio else "N/A",
                'peg_ratio': f"{peg_ratio:.2f}" if peg_ratio else "N/A",
                'ev_ebitda': f"{ev_ebitda:.2f}" if ev_ebitda else "N/A",
                'assessment': assessment
            },
            'score': score
        }
    
    def analyze_earnings_forecast(self) -> Dict[str, Any]:
        """
        Q10: 未来的盈利预测和当前价格匹配吗？
        Do future earnings forecasts match current price?
        """
        forward_pe = self.info.get('forwardPE', 0)
        trailing_pe = self.info.get('trailingPE', 0)
        earnings_growth = self.info.get('earningsGrowth', 0) * 100
        target_mean_price = self.info.get('targetMeanPrice', 0)
        current_price = self.info.get('currentPrice', 0)
        
        score = 50
        assessment = "Fair alignment"
        
        # Compare forward vs trailing P/E
        if forward_pe > 0 and trailing_pe > 0:
            pe_change = ((forward_pe - trailing_pe) / trailing_pe * 100)
            
            if pe_change < -10:
                score = 75
                assessment = "Improving earnings outlook - Forward P/E lower than trailing"
            elif pe_change < 10:
                score = 55
                assessment = "Stable earnings outlook"
            else:
                score = 35
                assessment = "Deteriorating earnings outlook"
        
        # Compare current price to analyst target
        if target_mean_price > 0 and current_price > 0:
            upside = ((target_mean_price - current_price) / current_price * 100)
            
            if upside > 20:
                score = min(100, score + 20)
                assessment += f" with {upside:.1f}% upside to target"
            elif upside < -10:
                score = max(0, score - 15)
                assessment += f" with {abs(upside):.1f}% downside to target"
        
        return {
            'question_en': 'Do future earnings forecasts match current price?',
            'question_zh': '未来的盈利预测和当前价格匹配吗？',
            'answer': {
                'forward_pe': f"{forward_pe:.2f}" if forward_pe else "N/A",
                'trailing_pe': f"{trailing_pe:.2f}" if trailing_pe else "N/A",
                'earnings_growth': f"{earnings_growth:.2f}%" if earnings_growth else "N/A",
                'target_price': f"${target_mean_price:.2f}" if target_mean_price else "N/A",
                'current_price': f"${current_price:.2f}",
                'assessment': assessment
            },
            'score': score
        }
    
    def get_all_analyses(self) -> List[Dict]:
        """Get all valuation analyses"""
        return [
            self.analyze_pe_pb_ratios(),
            self.analyze_historical_valuation(),
            self.analyze_peer_valuation(),
            self.analyze_earnings_forecast()
        ]
