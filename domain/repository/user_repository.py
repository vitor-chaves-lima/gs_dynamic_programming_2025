from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..model.user import User
from ..utils.uuid import uuid_to_bytes, bytes_to_uuid_str


class UserRepositoryImpl:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> None:
        self.session.add(user)
        await self.session.flush()
        await self.session.commit()

    async def find_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_by_id(self, user_id: str) -> Optional[User]:
        user_id_bytes = uuid_to_bytes(user_id)
        stmt = select(User).where(User.id == user_id_bytes)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()