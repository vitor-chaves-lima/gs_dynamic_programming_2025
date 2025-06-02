import datetime
import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.oracle import RAW
from sqlalchemy.orm import relationship
from .base import Base, SoftDeleteMixin

class UserScore(Base, SoftDeleteMixin):
    __tablename__ = 'user_scores'

    id = Column(RAW(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    user_id = Column(RAW(16), ForeignKey('users.id'), nullable=False)
    total_score = Column(Integer, default=0, nullable=False)
    total_questions = Column(Integer, default=0, nullable=False)
    correct_answers = Column(Integer, default=0, nullable=False)
    quiz_session_id = Column(String(36), nullable=True)
    completed_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False)

    user = relationship("User", back_populates="user_scores")

    @property
    def accuracy_percentage(self):
        if self.total_questions == 0:
            return 0
        return (self.correct_answers / self.total_questions) * 100
