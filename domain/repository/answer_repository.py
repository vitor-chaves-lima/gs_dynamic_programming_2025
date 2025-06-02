from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..model.answer import Answer
from ..utils.uuid import uuid_to_bytes


class AnswerRepositoryImpl:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, answer: Answer) -> None:
        await self.session.merge(answer)
        await self.session.commit()

    async def find_by_id(self, answer_id: str) -> Optional[Answer]:
        answer_id_bytes = uuid_to_bytes(answer_id)
        stmt = select(Answer).where(Answer.id == answer_id_bytes)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_by_question_id(self, question_id: str) -> List[Answer]:
        question_id_bytes = uuid_to_bytes(question_id)
        stmt = select(Answer).where(Answer.question_id == question_id_bytes)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())