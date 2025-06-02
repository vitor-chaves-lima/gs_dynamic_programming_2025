from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..model.user_score import UserScore
from ..utils.uuid import uuid_to_bytes


class UserScoreRepositoryImpl:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user_score: UserScore) -> None:
        await self.session.merge(user_score)
        await self.session.commit()

    async def find_by_user_id(self, user_id: str) -> Optional[UserScore]:
        user_id_bytes = uuid_to_bytes(user_id)
        stmt = select(UserScore).where(UserScore.user_id == user_id_bytes)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def find_all(self) -> List[UserScore]:
        stmt = select(UserScore)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())