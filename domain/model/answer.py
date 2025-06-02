import uuid
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.oracle import RAW
from sqlalchemy.orm import relationship
from .base import Base, SoftDeleteMixin

class Answer(Base, SoftDeleteMixin):
    __tablename__ = 'answers'

    id = Column(RAW(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    question_id = Column(RAW(16), ForeignKey('questions.id'), nullable=False)
    text = Column(String(1000), nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)
    order_position = Column(Integer, nullable=True)

    question = relationship("Question", back_populates="answers")
    user_answers = relationship("UserAnswer", back_populates="answer")
