from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UserOutput:
    id: str
    username: str
    email: str
    first_name: str
    last_name: str

@dataclass
class LoginOutput:
    user_id: str
    username: str
    email: str
    access_token: str
    expires_in: int

@dataclass
class UserScoreOutput:
    total_score: int
    total_questions: int
    correct_answers: int
    accuracy_percentage: float
    last_completed_at: Optional[str] = None