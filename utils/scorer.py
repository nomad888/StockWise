"""
Scoring and recommendation engine
"""
from typing import Dict, List, Tuple
import config

class Scorer:
    """Calculate scores and generate buy/sell recommendations"""
    
    def __init__(self):
        self.scores = {
            'fundamental': [],
            'valuation': [],
            'dividend': [],
            'technical': [],
            'sentiment': []
        }
        self.details = {
            'fundamental': [],
            'valuation': [],
            'dividend': [],
            'technical': [],
            'sentiment': []
        }
    
    def add_score(self, category: str, score: float, detail: str = ""):
        """
        Add a score to a category
        Args:
            category: One of 'fundamental', 'valuation', 'dividend', 'technical', 'sentiment'
            score: Score value (0-100)
            detail: Description of what this score represents
        """
        if category in self.scores:
            self.scores[category].append(max(0, min(100, score)))
            if detail:
                self.details[category].append(detail)
    
    def get_category_score(self, category: str) -> float:
        """Get average score for a category"""
        if category in self.scores and self.scores[category]:
            return sum(self.scores[category]) / len(self.scores[category])
        return 50.0  # Neutral score if no data
    
    def get_weighted_score(self) -> float:
        """Calculate final weighted score"""
        total_score = 0.0
        total_weight = 0.0
        
        for category, weight in config.WEIGHTS.items():
            category_score = self.get_category_score(category)
            total_score += category_score * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 50.0
    
    def get_recommendation(self) -> Tuple[str, str, str]:
        """
        Get buy/sell recommendation based on weighted score
        Returns: (recommendation_en, recommendation_zh, confidence)
        """
        score = self.get_weighted_score()
        
        if score >= config.THRESHOLDS['strong_buy']:
            return "Strong Buy", "强烈买入", "High"
        elif score >= config.THRESHOLDS['buy']:
            return "Buy", "买入", "Medium-High"
        elif score >= config.THRESHOLDS['hold']:
            return "Hold", "持有", "Medium"
        elif score >= config.THRESHOLDS['sell']:
            return "Sell", "卖出", "Medium-High"
        else:
            return "Strong Sell", "强烈卖出", "High"
    
    def get_score_breakdown(self) -> Dict[str, float]:
        """Get breakdown of scores by category"""
        return {
            category: self.get_category_score(category)
            for category in self.scores.keys()
        }
    
    def get_detailed_analysis(self) -> Dict[str, List[str]]:
        """Get detailed analysis points for each category"""
        return self.details
    
    def get_summary(self) -> Dict:
        """Get complete scoring summary"""
        rec_en, rec_zh, confidence = self.get_recommendation()
        
        return {
            'overall_score': round(self.get_weighted_score(), 2),
            'recommendation_en': rec_en,
            'recommendation_zh': rec_zh,
            'confidence': confidence,
            'category_scores': {k: round(v, 2) for k, v in self.get_score_breakdown().items()},
            'details': self.get_detailed_analysis()
        }
