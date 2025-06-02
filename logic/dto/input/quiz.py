from dataclasses import dataclass
from typing import Optional

@dataclass
class SubmitAnswerInput:
    question_id: str
    answer_id: str