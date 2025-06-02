import uuid
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.oracle import RAW
from sqlalchemy.orm import relationship
from .base import Base, SoftDeleteMixin

class Question(Base, SoftDeleteMixin):
    __tablename__ = 'questions'

    id = Column(RAW(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    title = Column(String(255), nullable=False)
    description = Column(String(2000), nullable=True)
    points = Column(Integer, default=1, nullable=False)
    difficulty_level = Column(String(20), default='medium', nullable=False)
    category = Column(String(50), nullable=True)

    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")
    user_answers = relationship("UserAnswer", back_populates="question")