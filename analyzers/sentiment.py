"""
Sentiment and News Analysis Module (Questions 17-20)
"""
from typing import Dict, Any, List
import pandas as pd
from datetime import datetime, timedelta

class SentimentAnalyzer:
    """Analyze market sentiment and news about a stock"""
    
    def __init__(self, data_fetcher):
        self.fetcher = data_fetcher
        self.info = data_fetcher.get_stock_info()
        self.news = data_fetcher.get_news()
        self.recommendations = data_fetcher.get_recommendations()
    
    def analyze_news(self) -> Dict[str, Any]:
        """
        Q17: 最近有没有和这家公司相关的重大新闻或公告？
        Are there any recent major news or announcements about this company?
        """
        score = 50
        news_summary = []
        
        if self.news and len(self.news) > 0:
            # Get recent news (last 7 days)
            recent_news = []
            for item in self.news[:5]:  # Top 5 news items
                title = item.get('title', 'No title')
                publisher = item.get('publisher', 'Unknown')
                link = item.get('link', '')
                
                # Try to get published time
                pub_time = item.get('providerPublishTime', 0)
                if pub_time:
                    pub_date = datetime.fromtimestamp(pub_time).strftime('%Y-%m-%d')
                else:
                    pub_date = 'Recent'
                
                recent_news.append({
                    'date': pub_date,
                    'title': title,
                    'publisher': publisher
                })
                news_summary.append(f"[{pub_date}] {title}")
            
            # Simple sentiment analysis based on keywords
            positive_keywords = ['beat', 'exceed', 'growth', 'profit', 'gain', 'rise', 'upgrade', 'buy', 'strong']
            negative_keywords = ['miss', 'decline', 'loss', 'fall', 'downgrade', 'sell', 'weak', 'concern']
            
            all_titles = ' '.join([item.get('title', '').lower() for item in self.news[:5]])
            
            positive_count = sum(1 for word in positive_keywords if word in all_titles)
            negative_count = sum(1 for word in negative_keywords if word in all_titles)
            
            if positive_count > negative_count:
                score = 70
                sentiment = "Positive news sentiment"
            elif negative_count > positive_count:
                score = 35
                sentiment = "Negative news sentiment"
            else:
                score = 50
                sentiment = "Neutral news sentiment"
            
            return {
                'question_en': 'Are there any recent major news or announcements about this company?',
                'question_zh': '最近有没有和这家公司相关的重大新闻或公告？',
                'answer': {
                    'news_count': len(self.news),
                    'recent_headlines': news_summary[:3],
                    'sentiment': sentiment
                },
                'score': score
            }
        
        return {
            'question_en': 'Are there any recent major news or announcements?',
            'question_zh': '最近有没有和这家公司相关的重大新闻或公告？',
            'answer': {
                'news_count': 0,
                'recent_headlines': ['No recent news available'],
                'sentiment': 'No data'
            },
            'score': 50
        }
    
    def analyze_analyst_ratings(self) -> Dict[str, Any]:
        """
        Q18: 分析师是看多还是看空这家公司？一致目标价是多少？
        Are analysts bullish or bearish? What is the consensus target price?
        """
        target_mean_price = self.info.get('targetMeanPrice', 0)
        target_high_price = self.info.get('targetHighPrice', 0)
        target_low_price = self.info.get('targetLowPrice', 0)
        current_price = self.info.get('currentPrice', 0)
        recommendation = self.info.get('recommendationKey', 'none')
        number_of_analysts = self.info.get('numberOfAnalystOpinions', 0)
        
        score = 50
        sentiment = "Neutral"
        
        # Calculate upside potential
        upside = 0
        if target_mean_price > 0 and current_price > 0:
            upside = ((target_mean_price - current_price) / current_price * 100)
            
            if upside > 20:
                score = 85
                sentiment = "Strong Buy - Significant upside"
            elif upside > 10:
                score = 70
                sentiment = "Buy - Moderate upside"
            elif upside > 0:
                score = 55
                sentiment = "Hold - Limited upside"
            elif upside > -10:
                score = 40
                sentiment = "Hold - Limited downside"
            else:
                score = 25
                sentiment = "Sell - Significant downside"
        
        # Adjust based on recommendation key
        if recommendation == 'buy' or recommendation == 'strong_buy':
            score = min(100, score + 10)
        elif recommendation == 'sell' or recommendation == 'strong_sell':
            score = max(0, score - 10)
        
        # Get recent analyst recommendations if available
        recent_ratings = []
        if self.recommendations is not None and not self.recommendations.empty:
            recent = self.recommendations.head(5)
            for idx, row in recent.iterrows():
                firm = row.get('Firm', 'Unknown')
                to_grade = row.get('To Grade', 'N/A')
                recent_ratings.append(f"{firm}: {to_grade}")
        
        return {
            'question_en': 'Are analysts bullish or bearish? What is the consensus target price?',
            'question_zh': '分析师是看多还是看空这家公司？一致目标价是多少？',
            'answer': {
                'consensus_rating': recommendation.replace('_', ' ').title(),
                'target_mean_price': f"${target_mean_price:.2f}" if target_mean_price else "N/A",
                'target_range': f"${target_low_price:.2f} - ${target_high_price:.2f}" if target_low_price and target_high_price else "N/A",
                'current_price': f"${current_price:.2f}",
                'upside_potential': f"{upside:+.2f}%" if upside else "N/A",
                'number_of_analysts': number_of_analysts,
                'sentiment': sentiment,
                'recent_ratings': recent_ratings[:3] if recent_ratings else ['No recent ratings available']
            },
            'score': score
        }
    
    def analyze_social_sentiment(self) -> Dict[str, Any]:
        """
        Q19: 社交媒体、股吧、论坛对这只股票情绪偏向乐观还是悲观？
        Is social media/forum sentiment optimistic or pessimistic about this stock?
        """
        # Note: Without API access to social media, this is limited
        # We can use news sentiment as a proxy
        
        score = 50
        sentiment = "Neutral"
        
        # Use news sentiment as proxy for social sentiment
        if self.news and len(self.news) > 0:
            positive_keywords = ['bullish', 'optimistic', 'positive', 'confident', 'strong buy']
            negative_keywords = ['bearish', 'pessimistic', 'negative', 'concerned', 'sell']
            
            all_text = ' '.join([item.get('title', '').lower() for item in self.news[:10]])
            
            positive_count = sum(1 for word in positive_keywords if word in all_text)
            negative_count = sum(1 for word in negative_keywords if word in all_text)
            
            if positive_count > negative_count:
                score = 65
                sentiment = "Leaning optimistic based on news tone"
            elif negative_count > positive_count:
                score = 40
                sentiment = "Leaning pessimistic based on news tone"
            else:
                score = 50
                sentiment = "Mixed/Neutral sentiment"
        
        return {
            'question_en': 'Is social media/forum sentiment optimistic or pessimistic?',
            'question_zh': '社交媒体、股吧、论坛对这只股票情绪偏向乐观还是悲观？',
            'answer': {
                'sentiment': sentiment,
                'note': 'Social sentiment analysis requires API access to social platforms. This assessment is based on news tone as a proxy.',
                'recommendation': 'For detailed social sentiment, consider using platforms like StockTwits, Reddit sentiment tools, or Twitter analysis.'
            },
            'score': score
        }
    
    def analyze_risk_events(self) -> Dict[str, Any]:
        """
        Q20: 近期有没有突发事件、监管政策或行业黑天鹅？
        Are there any recent unexpected events, regulatory policies, or industry black swans?
        """
        score = 50
        risk_factors = []
        
        # Check for risk-related keywords in news
        if self.news and len(self.news) > 0:
            risk_keywords = ['investigation', 'lawsuit', 'regulatory', 'scandal', 'fraud', 'recall', 
                           'bankruptcy', 'default', 'suspension', 'delisting', 'warning', 'violation']
            
            for item in self.news[:10]:
                title = item.get('title', '').lower()
                for keyword in risk_keywords:
                    if keyword in title:
                        risk_factors.append(f"⚠️ {item.get('title', 'Risk event detected')}")
                        score = max(0, score - 15)
                        break
        
        # Check company risk from info
        audit_risk = self.info.get('auditRisk', 0)
        board_risk = self.info.get('boardRisk', 0)
        compensation_risk = self.info.get('compensationRisk', 0)
        shareholder_risk = self.info.get('shareHolderRightsRisk', 0)
        overall_risk = self.info.get('overallRisk', 0)
        
        if overall_risk > 7:
            risk_factors.append(f"High overall risk score: {overall_risk}/10")
            score = max(0, score - 10)
        elif overall_risk > 0:
            risk_factors.append(f"Moderate overall risk score: {overall_risk}/10")
        
        if not risk_factors:
            risk_factors.append("No significant risk events detected in recent news")
            score = 60
        
        assessment = "High risk" if score < 40 else "Moderate risk" if score < 55 else "Low risk"
        
        return {
            'question_en': 'Are there any recent unexpected events, regulatory policies, or industry black swans?',
            'question_zh': '近期有没有突发事件、监管政策或行业黑天鹅？',
            'answer': {
                'risk_factors': risk_factors,
                'overall_risk_score': f"{overall_risk}/10" if overall_risk else "N/A",
                'assessment': assessment,
                'note': 'Risk assessment based on news analysis and company risk metrics'
            },
            'score': score
        }
    
    def get_all_analyses(self) -> List[Dict]:
        """Get all sentiment analyses"""
        return [
            self.analyze_news(),
            self.analyze_analyst_ratings(),
            self.analyze_social_sentiment(),
            self.analyze_risk_events()
        ]
