from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..model.question import Question
from ..utils.uuid import uuid_to_bytes


class QuestionRepositoryImpl:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, question: Question) -> None:
        await self.session.merge(question)
        await self.session.commit()

    async def find_by_id(self, question_id: str) -> Optional[Question]:
        question_id_bytes = uuid_to_bytes(question_id)
        stmt = select(Question).where(Question.id == question_id_bytes)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_all_active(self) -> List[Question]:
        stmt = select(Question).where(Question.is_deleted == False)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
