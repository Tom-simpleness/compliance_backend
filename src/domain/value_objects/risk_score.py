from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class RiskScore:
    score: int
    last_updated: datetime = datetime.utcnow()

    def __post_init__(self):
        if not 0 <= self.score <= 100:
            raise ValueError("Risk score must be between 0 and 100")