"""
Report Generator - Creates bilingual reports from analysis results
"""
from typing import Dict, Any
from datetime import datetime
import config

class ReportGenerator:
    """Generate formatted reports from stock analysis results"""
    
    def __init__(self, analysis_results: Dict[str, Any]):
        self.results = analysis_results
        self.symbol = analysis_results['symbol']
        self.company_name = analysis_results['company_name']
        self.summary = analysis_results['summary']
        self.all_results = analysis_results['results']
    
    def generate_report(self) -> str:
        """Generate complete bilingual report"""
        report = []
        
        # Header
        report.append(self._generate_header())
        
        # Executive Summary
        report.append(self._generate_executive_summary())
        
        # Detailed Analysis
        report.append(self._generate_detailed_analysis())
        
        # Recommendation
        report.append(self._generate_recommendation())
        
        # Footer
        report.append(self._generate_footer())
        
        return '\n'.join(report)
    
    def _generate_header(self) -> str:
        """Generate report header"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return f"""
{'='*100}
                        STOCK ANALYSIS REPORT | 股票分析报告
{'='*100}

Symbol | 股票代码: {self.symbol}
Company | 公司名称: {self.company_name}
Report Date | 报告日期: {timestamp}

{'='*100}
"""
    
    def _generate_executive_summary(self) -> str:
        """Generate executive summary section"""
        rec_en = self.summary['recommendation_en']
        rec_zh = self.summary['recommendation_zh']
        overall_score = self.summary['overall_score']
        confidence = self.summary['confidence']
        category_scores = self.summary['category_scores']
        
        # Create score bar
        score_bar = self._create_score_bar(overall_score)
        
        summary = f"""
{'─'*100}
EXECUTIVE SUMMARY | 执行摘要
{'─'*100}

Overall Score | 综合评分: {overall_score}/100
{score_bar}

Recommendation | 投资建议: {rec_en} | {rec_zh}
Confidence Level | 置信度: {confidence}

Category Breakdown | 分类评分:
  • Fundamental Analysis | 基本面分析:  {category_scores['fundamental']:.1f}/100
  • Valuation Analysis | 估值分析:      {category_scores['valuation']:.1f}/100
  • Dividend Analysis | 分红分析:       {category_scores['dividend']:.1f}/100
  • Technical Analysis | 技术分析:      {category_scores['technical']:.1f}/100
  • Sentiment Analysis | 情绪分析:      {category_scores['sentiment']:.1f}/100

"""
        return summary
    
    def _generate_detailed_analysis(self) -> str:
        """Generate detailed Q&A section"""
        sections = []
        
        sections.append(f"""
{'─'*100}
DETAILED ANALYSIS | 详细分析
{'─'*100}
""")
        
        # Group results by category
        categories = {
            'FUNDAMENTAL ANALYSIS | 基本面分析 (Q1-Q6)': list(range(0, 6)),
            'VALUATION ANALYSIS | 估值分析 (Q7-Q10)': list(range(6, 10)),
            'DIVIDEND ANALYSIS | 分红分析 (Q11)': list(range(10, 11)),
            'TECHNICAL ANALYSIS | 技术分析 (Q12-Q16)': list(range(11, 16)),
            'SENTIMENT ANALYSIS | 情绪分析 (Q17-Q20)': list(range(16, 20))
        }
        
        for category_name, indices in categories.items():
            sections.append(f"\n{'─'*100}")
            sections.append(f"{category_name}")
            sections.append(f"{'─'*100}\n")
            
            for i, idx in enumerate(indices, 1):
                if idx < len(self.all_results):
                    result = self.all_results[idx]
                    sections.append(self._format_question(result, idx + 1))
        
        return '\n'.join(sections)
    
    def _format_question(self, result: Dict, question_num: int) -> str:
        """Format a single question and answer"""
        question_en = result.get('question_en', 'N/A')
        question_zh = result.get('question_zh', 'N/A')
        answer = result.get('answer', {})
        score = result.get('score', 'N/A')
        
        output = [f"\nQ{question_num}. {question_en}"]
        output.append(f"    {question_zh}")
        
        if score != 'N/A':
            score_indicator = self._get_score_indicator(score)
            output.append(f"    Score | 得分: {score}/100 {score_indicator}")
        
        output.append(f"\n    Answer | 回答:")
        
        # Format answer based on type
        if isinstance(answer, dict):
            for key, value in answer.items():
                # Format key nicely
                formatted_key = key.replace('_', ' ').title()
                
                # Handle list values
                if isinstance(value, list):
                    output.append(f"      • {formatted_key}:")
                    for item in value:
                        output.append(f"        - {item}")
                else:
                    output.append(f"      • {formatted_key}: {value}")
        else:
            output.append(f"      {answer}")
        
        output.append("")  # Empty line
        
        return '\n'.join(output)
    
    def _generate_recommendation(self) -> str:
        """Generate final recommendation section"""
        rec_en = self.summary['recommendation_en']
        rec_zh = self.summary['recommendation_zh']
        overall_score = self.summary['overall_score']
        
        # Generate recommendation explanation
        if overall_score >= 75:
            explanation_en = "Strong fundamentals, attractive valuation, positive technical signals, and favorable sentiment."
            explanation_zh = "基本面强劲，估值吸引，技术信号积极，市场情绪良好。"
        elif overall_score >= 60:
            explanation_en = "Good fundamentals with reasonable valuation. Consider buying on dips."
            explanation_zh = "基本面良好，估值合理。可考虑逢低买入。"
        elif overall_score >= 40:
            explanation_en = "Mixed signals. Current position holders may hold, but new entry not recommended."
            explanation_zh = "信号混合。持仓者可继续持有，但不建议新进场。"
        elif overall_score >= 25:
            explanation_en = "Weak fundamentals or unfavorable conditions. Consider reducing position."
            explanation_zh = "基本面疲弱或条件不利。考虑减仓。"
        else:
            explanation_en = "Significant concerns identified. Consider exiting position."
            explanation_zh = "发现重大问题。考虑退出。"
        
        recommendation = f"""
{'─'*100}
FINAL RECOMMENDATION | 最终建议
{'─'*100}

Recommendation | 建议: {rec_en} | {rec_zh}

Rationale | 理由:
  English: {explanation_en}
  中文: {explanation_zh}

Risk Warning | 风险提示:
  This analysis is for reference only and does not constitute investment advice.
  Please conduct your own due diligence and consult with financial professionals.
  
  本分析仅供参考，不构成投资建议。
  请进行自己的尽职调查并咨询专业人士。

{'='*100}
"""
        return recommendation
    
    def _generate_footer(self) -> str:
        """Generate report footer"""
        return f"""
Report generated by StockWise Analysis System
Powered by yfinance and technical analysis libraries

Data sources: Yahoo Finance, Public market data
Analysis methodology: Multi-factor quantitative scoring system

{'='*100}
"""
    
    def _create_score_bar(self, score: float) -> str:
        """Create a visual score bar"""
        filled = int(score / 5)  # 20 blocks for 100 points
        empty = 20 - filled
        
        bar = '█' * filled + '░' * empty
        return f"[{bar}]"
    
    def _get_score_indicator(self, score: float) -> str:
        """Get emoji indicator for score"""
        if score >= 75:
            return "🟢 Excellent"
        elif score >= 60:
            return "🔵 Good"
        elif score >= 40:
            return "🟡 Fair"
        elif score >= 25:
            return "🟠 Poor"
        else:
            return "🔴 Very Poor"
    
    def save_report(self, filename: str = None):
        """Save report to file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.symbol}_analysis_{timestamp}.txt"
        
        report = self.generate_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📄 Report saved to: {filename}")
        return filename
