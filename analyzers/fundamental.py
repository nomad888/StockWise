"""
Fundamental Analysis Module (Questions 1-6)
"""
from typing import Dict, Any, List
import pandas as pd
import numpy as np

class FundamentalAnalyzer:
    """Analyze fundamental aspects of a stock"""
    
    def __init__(self, data_fetcher):
        self.fetcher = data_fetcher
        self.info = data_fetcher.get_stock_info()
        self.financials = data_fetcher.get_financials()
    
    def analyze_business(self) -> Dict[str, Any]:
        """
        Q1: 这家公司主要是做什么的？核心产品或服务是什么？
        What does this company do? What are its core products/services?
        """
        business_summary = self.info.get('longBusinessSummary', 'N/A')
        sector = self.info.get('sector', 'N/A')
        industry = self.info.get('industry', 'N/A')
        
        return {
            'question_en': 'What does this company do? What are its core products/services?',
            'question_zh': '这家公司主要是做什么的？核心产品或服务是什么？',
            'answer': {
                'sector': sector,
                'industry': industry,
                'business_summary': business_summary,
                'company_name': self.info.get('longName', self.fetcher.symbol)
            }
        }
    
    def analyze_profitability(self) -> Dict[str, Any]:
        """
        Q2: 它的盈利能力强吗？净利润和毛利率近几年变化如何？
        Is profitability strong? How have net profit and gross margin changed in recent years?
        """
        profit_margin = self.info.get('profitMargins', 0) * 100
        gross_margin = self.info.get('grossMargins', 0) * 100
        
        # Try to get historical margins from financials
        margins_trend = "N/A"
        score = 50
        
        try:
            if 'income_stmt' in self.financials and not self.financials['income_stmt'].empty:
                income_stmt = self.financials['income_stmt']
                
                if 'Gross Profit' in income_stmt.index and 'Total Revenue' in income_stmt.index:
                    gross_profits = income_stmt.loc['Gross Profit']
                    revenues = income_stmt.loc['Total Revenue']
                    historical_margins = (gross_profits / revenues * 100).dropna()
                    
                    if len(historical_margins) >= 2:
                        trend = "improving" if historical_margins.iloc[0] > historical_margins.iloc[-1] else "declining"
                        margins_trend = f"{trend} ({historical_margins.iloc[-1]:.1f}% → {historical_margins.iloc[0]:.1f}%)"
                        
                        # Score based on margin level and trend
                        if gross_margin > 40:
                            score = 80 if trend == "improving" else 70
                        elif gross_margin > 25:
                            score = 65 if trend == "improving" else 55
                        else:
                            score = 45 if trend == "improving" else 35
        except Exception as e:
            print(f"Error analyzing profitability trend: {e}")
        
        # Adjust score based on current margins
        if profit_margin > 20:
            score = min(100, score + 10)
        elif profit_margin < 5:
            score = max(0, score - 15)
        
        return {
            'question_en': 'Is profitability strong? Net profit and gross margin trends?',
            'question_zh': '它的盈利能力强吗？净利润和毛利率近几年变化如何？',
            'answer': {
                'profit_margin': f"{profit_margin:.2f}%",
                'gross_margin': f"{gross_margin:.2f}%",
                'margins_trend': margins_trend,
                'assessment': 'Strong' if profit_margin > 15 else 'Moderate' if profit_margin > 5 else 'Weak'
            },
            'score': score
        }
    
    def analyze_revenue_growth(self) -> Dict[str, Any]:
        """
        Q3: 它的营收增长稳不稳？同比和环比增长如何？
        Is revenue growth stable? YoY and QoQ growth?
        """
        revenue_growth = self.info.get('revenueGrowth', 0) * 100
        quarterly_revenue_growth = self.info.get('quarterlyRevenueGrowth', 0) * 100
        
        score = 50
        stability = "Moderate"
        
        # Score based on growth rates
        if revenue_growth > 20:
            score = 85
            stability = "Strong growth"
        elif revenue_growth > 10:
            score = 70
            stability = "Healthy growth"
        elif revenue_growth > 0:
            score = 55
            stability = "Modest growth"
        elif revenue_growth > -5:
            score = 40
            stability = "Stagnant"
        else:
            score = 25
            stability = "Declining"
        
        return {
            'question_en': 'Is revenue growth stable? YoY and QoQ growth?',
            'question_zh': '它的营收增长稳不稳？同比和环比增长如何？',
            'answer': {
                'yoy_growth': f"{revenue_growth:.2f}%",
                'qoq_growth': f"{quarterly_revenue_growth:.2f}%",
                'stability': stability
            },
            'score': score
        }
    
    def analyze_balance_sheet(self) -> Dict[str, Any]:
        """
        Q4: 资产负债情况怎么样？有没有高杠杆风险？
        How is the balance sheet? Any high leverage risk?
        """
        debt_to_equity = self.info.get('debtToEquity', 0)
        current_ratio = self.info.get('currentRatio', 0)
        quick_ratio = self.info.get('quickRatio', 0)
        
        score = 50
        risk_level = "Moderate"
        
        # Assess leverage risk
        if debt_to_equity < 50:
            score = 85
            risk_level = "Low leverage - Healthy"
        elif debt_to_equity < 100:
            score = 65
            risk_level = "Moderate leverage - Acceptable"
        elif debt_to_equity < 200:
            score = 45
            risk_level = "High leverage - Caution"
        else:
            score = 25
            risk_level = "Very high leverage - Risky"
        
        # Adjust for liquidity
        if current_ratio > 2:
            score = min(100, score + 10)
        elif current_ratio < 1:
            score = max(0, score - 15)
        
        return {
            'question_en': 'How is the balance sheet? Any high leverage risk?',
            'question_zh': '资产负债情况怎么样？有没有高杠杆风险？',
            'answer': {
                'debt_to_equity': f"{debt_to_equity:.2f}",
                'current_ratio': f"{current_ratio:.2f}",
                'quick_ratio': f"{quick_ratio:.2f}",
                'risk_level': risk_level
            },
            'score': score
        }
    
    def analyze_cash_flow(self) -> Dict[str, Any]:
        """
        Q5: 现金流是否充足？经营活动现金流为正吗？
        Is cash flow sufficient? Is operating cash flow positive?
        """
        operating_cashflow = self.info.get('operatingCashflow', 0)
        free_cashflow = self.info.get('freeCashflow', 0)
        
        score = 50
        assessment = "Moderate"
        
        if operating_cashflow > 0 and free_cashflow > 0:
            score = 80
            assessment = "Strong - Both operating and free cash flow positive"
        elif operating_cashflow > 0:
            score = 60
            assessment = "Adequate - Operating cash flow positive"
        elif operating_cashflow == 0:
            score = 50
            assessment = "Unknown - Data not available"
        else:
            score = 30
            assessment = "Weak - Negative cash flow"
        
        return {
            'question_en': 'Is cash flow sufficient? Is operating cash flow positive?',
            'question_zh': '现金流是否充足？经营活动现金流为正吗？',
            'answer': {
                'operating_cashflow': f"${operating_cashflow:,.0f}" if operating_cashflow else "N/A",
                'free_cashflow': f"${free_cashflow:,.0f}" if free_cashflow else "N/A",
                'assessment': assessment
            },
            'score': score
        }
    
    def analyze_management(self) -> Dict[str, Any]:
        """
        Q6: 管理层和大股东背景如何？他们有没有长期持股？
        Management and major shareholder background? Long-term holdings?
        """
        holders = self.fetcher.get_major_holders()
        
        insider_ownership = 0
        institutional_ownership = 0
        
        try:
            if 'major_holders' in holders and holders['major_holders'] is not None:
                major_holders_df = holders['major_holders']
                if not major_holders_df.empty and len(major_holders_df) >= 2:
                    # Typically first row is % held by insiders, second is % held by institutions
                    insider_ownership = float(str(major_holders_df.iloc[0, 0]).rstrip('%'))
                    institutional_ownership = float(str(major_holders_df.iloc[1, 0]).rstrip('%'))
        except Exception as e:
            print(f"Error parsing holder data: {e}")
        
        score = 50
        assessment = "Moderate ownership structure"
        
        # Score based on insider and institutional ownership
        if insider_ownership > 10:
            score = 75
            assessment = "Strong insider ownership - Management aligned with shareholders"
        elif insider_ownership > 5:
            score = 65
            assessment = "Good insider ownership"
        
        if institutional_ownership > 60:
            score = min(100, score + 10)
            assessment += " with strong institutional backing"
        
        return {
            'question_en': 'Management and major shareholder background? Long-term holdings?',
            'question_zh': '管理层和大股东背景如何？他们有没有长期持股？',
            'answer': {
                'insider_ownership': f"{insider_ownership:.2f}%",
                'institutional_ownership': f"{institutional_ownership:.2f}%",
                'assessment': assessment
            },
            'score': score
        }
    
    def get_all_analyses(self) -> List[Dict]:
        """Get all fundamental analyses"""
        return [
            self.analyze_business(),
            self.analyze_profitability(),
            self.analyze_revenue_growth(),
            self.analyze_balance_sheet(),
            self.analyze_cash_flow(),
            self.analyze_management()
        ]
