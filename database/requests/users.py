from sqlalchemy.ext.asyncio import AsyncSession

from database import User
from bot.enums.roles import Role
from bot.enums.levels import Level


async def get_user(session: AsyncSession, tg_id: int) -> User:
    """Returns User by tg_id"""
    return await session.get(User, tg_id)


async def add_user(
    session: AsyncSession,
    tg_id: int,
    language: str,
    role: Role = Role.USER,
    level: Level = Level.FREE,
) -> None:
    """Adds User"""
    new_user = User(tg_id=tg_id, role=role, level=level, language=language)
    session.add(new_user)
    await session.commit()


async def set_role(
    session: AsyncSession,
    tg_id: int,
    role: Role,
) -> None:
    """Sets role for User"""
    user = await session.get(User, tg_id)
    user.role = role
    await session.commit()


async def set_level(
    session: AsyncSession,
    tg_id: int,
    level: Level,
) -> None:
    """Sets level for User"""
    user = await session.get(User, tg_id)
    user.level = level
    await session.commit()
