import math
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class QualityVote:
    voter_id: str
    timestamp: datetime
    score: float
    confidence: float
    
class ConsensusGovernance:
    def __init__(self, min_votes: int = 3, confidence_threshold: float = 0.7):
        self.min_votes = min_votes
        self.confidence_threshold = confidence_threshold
        self.votes: Dict[str, List[QualityVote]] = {}
        
    def submit_vote(self, code_id: str, voter_id: str, score: float, confidence: float) -> None:
        """Submit a quality vote for a specific code change"""
        if not 0 <= score <= 1 or not 0 <= confidence <= 1:
            raise ValueError('Score and confidence must be between 0 and 1')
            
        vote = QualityVote(
            voter_id=voter_id,
            timestamp=datetime.now(),
            score=score,
            confidence=confidence
        )
        
        if code_id not in self.votes:
            self.votes[code_id] = []
        self.votes[code_id].append(vote)
        
    def get_consensus(self, code_id: str) -> Tuple[float, bool]:
        """Calculate weighted consensus score and determine if change should be accepted"""
        if code_id not in self.votes:
            return 0.0, False
            
        votes = self.votes[code_id]
        if len(votes) < self.min_votes:
            return 0.0, False
            
        # Calculate weighted average based on confidence
        total_weight = 0.0
        weighted_sum = 0.0
        
        for vote in votes:
            weight = vote.confidence
            total_weight += weight
            weighted_sum += vote.score * weight
            
        consensus_score = weighted_sum / total_weight if total_weight > 0 else 0
        
        # Calculate agreement level
        variance = sum((v.score - consensus_score) ** 2 for v in votes) / len(votes)
        agreement = 1 - math.sqrt(variance)
        
        # Decision requires both high enough score and agreement
        should_accept = (consensus_score >= 0.75 and 
                        agreement >= self.confidence_threshold and
                        len(votes) >= self.min_votes)
                        
        return consensus_score, should_accept
        
    def get_vote_summary(self, code_id: str) -> Dict:
        """Get summary statistics for votes on a specific change"""
        if code_id not in self.votes:
            return {
                'total_votes': 0,
                'average_score': 0.0,
                'average_confidence': 0.0,
                'consensus_reached': False
            }
            
        votes = self.votes[code_id]
        consensus_score, consensus_reached = self.get_consensus(code_id)
        
        return {
            'total_votes': len(votes),
            'average_score': sum(v.score for v in votes) / len(votes),
            'average_confidence': sum(v.confidence for v in votes) / len(votes),
            'consensus_score': consensus_score,
            'consensus_reached': consensus_reached
        }
        
    def clear_votes(self, code_id: str) -> None:
        """Clear all votes for a specific code change"""
        if code_id in self.votes:
            del self.votes[code_id]