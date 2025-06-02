from dataclasses import dataclass
from typing import Optional

@dataclass
class GetRankingInput:
    limit: Optional[int] = 10
    category: Optional[str] = None