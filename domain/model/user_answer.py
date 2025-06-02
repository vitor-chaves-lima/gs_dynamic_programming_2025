import datetime
import uuid
from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.oracle import RAW
from sqlalchemy.orm import relationship
from .base import Base, SoftDeleteMixin

class UserAnswer(Base, SoftDeleteMixin):
    __tablename__ = 'user_answers'

    id = Column(RAW(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    user_id = Column(RAW(16), ForeignKey('users.id'), nullable=False)
    question_id = Column(RAW(16), ForeignKey('questions.id'), nullable=False)
    answer_id = Column(RAW(16), ForeignKey('answers.id'), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    points_earned = Column(Integer, default=0, nullable=False)
    answered_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False)

    user = relationship("User", back_populates="user_answers")
    question = relationship("Question", back_populates="user_answers")
    answer = relationship("Answer", back_populates="user_answers")