from dataclasses import dataclass
from typing import List

@dataclass
class RankingUserOutput:
    position: int
    user_id: str
    username: str
    total_score: int
    total_questions: int
    accuracy_percentage: float

@dataclass
class RankingOutput:
    users: List[RankingUserOutput]
    total_users: int