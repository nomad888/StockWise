"""
Technical Analysis Module (Questions 12-16)
"""
from typing import Dict, Any, List
import pandas as pd
import numpy as np
from ta.trend import MACD, SMAIndicator, EMAIndicator
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volume import OnBalanceVolumeIndicator
import config

class TechnicalAnalyzer:
    """Analyze technical indicators of a stock"""
    
    def __init__(self, data_fetcher):
        self.fetcher = data_fetcher
        self.info = data_fetcher.get_stock_info()
        self.history = data_fetcher.get_historical_data(period="1y")
    
    def analyze_price_trend(self) -> Dict[str, Any]:
        """
        Q12: 当前股价处于什么趋势？上涨、震荡还是下跌？
        What is the current price trend? Uptrend, sideways, or downtrend?
        """
        score = 50
        trend = "Unknown"
        
        if self.history is not None and not self.history.empty and len(self.history) > 50:
            close_prices = self.history['Close']
            
            # Calculate moving averages
            sma_20 = close_prices.rolling(window=20).mean()
            sma_50 = close_prices.rolling(window=50).mean()
            
            current_price = close_prices.iloc[-1]
            sma_20_current = sma_20.iloc[-1]
            sma_50_current = sma_50.iloc[-1]
            
            # Determine trend
            if current_price > sma_20_current > sma_50_current:
                trend = "Strong Uptrend"
                score = 85
            elif current_price > sma_20_current:
                trend = "Uptrend"
                score = 70
            elif current_price < sma_20_current < sma_50_current:
                trend = "Strong Downtrend"
                score = 20
            elif current_price < sma_20_current:
                trend = "Downtrend"
                score = 35
            else:
                trend = "Sideways/Consolidation"
                score = 50
            
            # Calculate price change percentages
            price_1m = close_prices.iloc[-21] if len(close_prices) > 21 else close_prices.iloc[0]
            price_3m = close_prices.iloc[-63] if len(close_prices) > 63 else close_prices.iloc[0]
            
            change_1m = ((current_price - price_1m) / price_1m * 100)
            change_3m = ((current_price - price_3m) / price_3m * 100)
            
            return {
                'question_en': 'What is the current price trend? Uptrend, sideways, or downtrend?',
                'question_zh': '当前股价处于什么趋势？上涨、震荡还是下跌？',
                'answer': {
                    'trend': trend,
                    'current_price': f"${current_price:.2f}",
                    '1_month_change': f"{change_1m:+.2f}%",
                    '3_month_change': f"{change_3m:+.2f}%",
                    'sma_20': f"${sma_20_current:.2f}",
                    'sma_50': f"${sma_50_current:.2f}"
                },
                'score': score
            }
        
        return {
            'question_en': 'What is the current price trend?',
            'question_zh': '当前股价处于什么趋势？上涨、震荡还是下跌？',
            'answer': {'trend': 'Insufficient data'},
            'score': 50
        }
    
    def analyze_technical_indicators(self) -> Dict[str, Any]:
        """
        Q13: 关键技术指标如MACD、RSI、KDJ怎么看？
        How do key technical indicators like MACD, RSI, KDJ look?
        """
        score = 50
        signals = []
        
        if self.history is not None and not self.history.empty and len(self.history) > 26:
            close_prices = self.history['Close']
            high_prices = self.history['High']
            low_prices = self.history['Low']
            
            # RSI
            rsi_indicator = RSIIndicator(close=close_prices, window=14)
            rsi = rsi_indicator.rsi().iloc[-1]
            
            if rsi < config.TECHNICAL_PARAMS['rsi_oversold']:
                signals.append(f"RSI oversold ({rsi:.1f}) - Bullish signal")
                score += 15
            elif rsi > config.TECHNICAL_PARAMS['rsi_overbought']:
                signals.append(f"RSI overbought ({rsi:.1f}) - Bearish signal")
                score -= 15
            else:
                signals.append(f"RSI neutral ({rsi:.1f})")
            
            # MACD
            macd_indicator = MACD(close=close_prices)
            macd = macd_indicator.macd().iloc[-1]
            macd_signal = macd_indicator.macd_signal().iloc[-1]
            macd_diff = macd_indicator.macd_diff().iloc[-1]
            
            if macd > macd_signal and macd_diff > 0:
                signals.append("MACD bullish crossover")
                score += 15
            elif macd < macd_signal and macd_diff < 0:
                signals.append("MACD bearish crossover")
                score -= 15
            else:
                signals.append("MACD neutral")
            
            # Stochastic (KDJ equivalent)
            stoch_indicator = StochasticOscillator(high=high_prices, low=low_prices, close=close_prices)
            stoch_k = stoch_indicator.stoch().iloc[-1]
            stoch_d = stoch_indicator.stoch_signal().iloc[-1]
            
            if stoch_k < 20:
                signals.append(f"Stochastic oversold ({stoch_k:.1f}) - Bullish")
                score += 10
            elif stoch_k > 80:
                signals.append(f"Stochastic overbought ({stoch_k:.1f}) - Bearish")
                score -= 10
            else:
                signals.append(f"Stochastic neutral ({stoch_k:.1f})")
            
            score = max(0, min(100, score))
            
            return {
                'question_en': 'How do key technical indicators like MACD, RSI, KDJ look?',
                'question_zh': '关键技术指标如MACD、RSI、KDJ怎么看？',
                'answer': {
                    'rsi': f"{rsi:.2f}",
                    'macd': f"{macd:.4f}",
                    'macd_signal': f"{macd_signal:.4f}",
                    'stochastic_k': f"{stoch_k:.2f}",
                    'stochastic_d': f"{stoch_d:.2f}",
                    'signals': signals
                },
                'score': score
            }
        
        return {
            'question_en': 'How do key technical indicators look?',
            'question_zh': '关键技术指标如MACD、RSI、KDJ怎么看？',
            'answer': {'signals': ['Insufficient data']},
            'score': 50
        }
    
    def analyze_chart_patterns(self) -> Dict[str, Any]:
        """
        Q14: 有没有形成重要的技术形态？如双底、头肩顶？
        Are there important technical patterns? Like double bottom, head and shoulders?
        """
        score = 50
        patterns = []
        
        if self.history is not None and not self.history.empty and len(self.history) > 60:
            close_prices = self.history['Close'].tail(60)
            high_prices = self.history['High'].tail(60)
            low_prices = self.history['Low'].tail(60)
            
            # Simple pattern detection (basic implementation)
            current_price = close_prices.iloc[-1]
            max_price = high_prices.max()
            min_price = low_prices.min()
            
            # Check for double bottom (simplified)
            recent_lows = low_prices.tail(30)
            if len(recent_lows) > 10:
                lowest_points = recent_lows.nsmallest(3)
                if len(lowest_points) >= 2:
                    if abs(lowest_points.iloc[0] - lowest_points.iloc[1]) / lowest_points.iloc[0] < 0.02:
                        patterns.append("Potential double bottom pattern (bullish)")
                        score += 15
            
            # Check for breakout
            sma_20 = close_prices.rolling(window=20).mean().iloc[-1]
            if current_price > sma_20 * 1.05:
                patterns.append("Price breaking above 20-day MA (bullish)")
                score += 10
            elif current_price < sma_20 * 0.95:
                patterns.append("Price breaking below 20-day MA (bearish)")
                score -= 10
            
            # Check for consolidation
            price_range = (max_price - min_price) / min_price * 100
            if price_range < 10:
                patterns.append("Tight consolidation - potential breakout setup")
                score += 5
            
            if not patterns:
                patterns.append("No significant patterns detected")
            
            score = max(0, min(100, score))
            
            return {
                'question_en': 'Are there important technical patterns? Like double bottom, head and shoulders?',
                'question_zh': '有没有形成重要的技术形态？如双底、头肩顶？',
                'answer': {
                    'patterns': patterns,
                    'note': 'Pattern detection is simplified - manual chart review recommended'
                },
                'score': score
            }
        
        return {
            'question_en': 'Are there important technical patterns?',
            'question_zh': '有没有形成重要的技术形态？如双底、头肩顶？',
            'answer': {'patterns': ['Insufficient data for pattern analysis']},
            'score': 50
        }
    
    def analyze_moving_averages(self) -> Dict[str, Any]:
        """
        Q15: 当前价格处于年线、季线、均线哪个区间？
        Where is the current price relative to annual, quarterly, and moving averages?
        """
        score = 50
        
        if self.history is not None and not self.history.empty and len(self.history) > 200:
            close_prices = self.history['Close']
            current_price = close_prices.iloc[-1]
            
            # Calculate moving averages
            ma_50 = close_prices.rolling(window=50).mean().iloc[-1]  # Quarterly line
            ma_200 = close_prices.rolling(window=200).mean().iloc[-1]  # Annual line
            ma_20 = close_prices.rolling(window=20).mean().iloc[-1]  # Monthly line
            
            position = []
            
            # Determine position
            if current_price > ma_200:
                position.append("Above 200-day MA (annual line) - Long-term uptrend")
                score = 75
            else:
                position.append("Below 200-day MA (annual line) - Long-term downtrend")
                score = 35
            
            if current_price > ma_50:
                position.append("Above 50-day MA (quarterly line) - Medium-term uptrend")
                score = min(100, score + 10)
            else:
                position.append("Below 50-day MA (quarterly line) - Medium-term downtrend")
                score = max(0, score - 10)
            
            # Golden cross / Death cross
            if ma_50 > ma_200:
                position.append("Golden Cross (50-day > 200-day) - Bullish")
                score = min(100, score + 10)
            elif ma_50 < ma_200:
                position.append("Death Cross (50-day < 200-day) - Bearish")
                score = max(0, score - 10)
            
            return {
                'question_en': 'Where is the current price relative to annual, quarterly, and moving averages?',
                'question_zh': '当前价格处于年线、季线、均线哪个区间？',
                'answer': {
                    'current_price': f"${current_price:.2f}",
                    'ma_20': f"${ma_20:.2f}",
                    'ma_50': f"${ma_50:.2f}",
                    'ma_200': f"${ma_200:.2f}",
                    'position': position
                },
                'score': score
            }
        
        return {
            'question_en': 'Where is the current price relative to moving averages?',
            'question_zh': '当前价格处于年线、季线、均线哪个区间？',
            'answer': {'position': ['Insufficient data']},
            'score': 50
        }
    
    def analyze_volume(self) -> Dict[str, Any]:
        """
        Q16: 近期成交量变化大吗？量价关系是否健康？
        Are there significant volume changes recently? Is price-volume relationship healthy?
        """
        score = 50
        
        if self.history is not None and not self.history.empty and len(self.history) > 20:
            volumes = self.history['Volume']
            close_prices = self.history['Close']
            
            # Calculate average volume
            avg_volume_20 = volumes.tail(20).mean()
            recent_volume = volumes.iloc[-1]
            volume_ratio = recent_volume / avg_volume_20 if avg_volume_20 > 0 else 1
            
            # Price change
            price_change = ((close_prices.iloc[-1] - close_prices.iloc[-2]) / close_prices.iloc[-2] * 100)
            
            assessment = []
            
            # Volume analysis
            if volume_ratio > 1.5:
                assessment.append(f"High volume ({volume_ratio:.1f}x average)")
                if price_change > 0:
                    assessment.append("Price up on high volume - Bullish confirmation")
                    score = 80
                else:
                    assessment.append("Price down on high volume - Bearish signal")
                    score = 30
            elif volume_ratio < 0.5:
                assessment.append(f"Low volume ({volume_ratio:.1f}x average)")
                assessment.append("Low conviction move")
                score = 45
            else:
                assessment.append("Normal volume")
                score = 55
            
            # On-Balance Volume trend
            obv_indicator = OnBalanceVolumeIndicator(close=close_prices, volume=volumes)
            obv = obv_indicator.on_balance_volume()
            obv_trend = "rising" if obv.iloc[-1] > obv.iloc[-10] else "falling"
            assessment.append(f"OBV trend: {obv_trend}")
            
            if obv_trend == "rising":
                score = min(100, score + 10)
            else:
                score = max(0, score - 10)
            
            return {
                'question_en': 'Are there significant volume changes? Is price-volume relationship healthy?',
                'question_zh': '近期成交量变化大吗？量价关系是否健康？',
                'answer': {
                    'recent_volume': f"{recent_volume:,.0f}",
                    'avg_volume_20d': f"{avg_volume_20:,.0f}",
                    'volume_ratio': f"{volume_ratio:.2f}x",
                    'price_change': f"{price_change:+.2f}%",
                    'assessment': assessment
                },
                'score': score
            }
        
        return {
            'question_en': 'Are there significant volume changes?',
            'question_zh': '近期成交量变化大吗？量价关系是否健康？',
            'answer': {'assessment': ['Insufficient data']},
            'score': 50
        }
    
    def get_all_analyses(self) -> List[Dict]:
        """Get all technical analyses"""
        return [
            self.analyze_price_trend(),
            self.analyze_technical_indicators(),
            self.analyze_chart_patterns(),
            self.analyze_moving_averages(),
            self.analyze_volume()
        ]
