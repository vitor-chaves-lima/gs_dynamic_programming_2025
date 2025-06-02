import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.oracle import RAW
from sqlalchemy.orm import relationship
from .base import Base, SoftDeleteMixin

class User(Base, SoftDeleteMixin):
    __tablename__ = 'users'

    id = Column(RAW(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    user_scores = relationship("UserScore", back_populates="user")
    user_answers = relationship("UserAnswer", back_populates="user")
