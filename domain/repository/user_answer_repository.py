from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..model.user_answer import UserAnswer
from ..utils.uuid import uuid_to_bytes


class UserAnswerRepositoryImpl:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user_answer: UserAnswer) -> None:
        await self.session.merge(user_answer)
        await self.session.commit()


    async def find_by_user_and_question(self, user_id: str, question_id: str) -> List[UserAnswer]:
        user_id_bytes = uuid_to_bytes(user_id)
        question_id_bytes = uuid_to_bytes(question_id)
        stmt = select(UserAnswer).where(
            UserAnswer.user_id == user_id_bytes,
            UserAnswer.question_id == question_id_bytes
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())