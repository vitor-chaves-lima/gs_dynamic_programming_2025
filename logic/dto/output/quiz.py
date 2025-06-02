from dataclasses import dataclass
from typing import List

@dataclass
class AnswerOutput:
    id: str
    text: str
    order_position: int

@dataclass
class QuestionOutput:
    id: str
    title: str
    description: str
    points: int
    difficulty_level: str
    category: str
    answers: List[AnswerOutput]

@dataclass
class SubmitAnswerOutput:
    is_correct: bool
    points_earned: int
    correct_answer_id: str
    explanation: str
    current_score: int
