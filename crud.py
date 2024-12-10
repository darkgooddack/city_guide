from sqlalchemy import cast, BigInteger
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from sqlalchemy.future import select


async def add_user(user_id: int, username: str, session: AsyncSession):
    new_user = User(
        telegram_id=user_id,
        username=username,
    )
    session.add(new_user)
    await session.commit()


async def check_user_exists(user_id: int, session: AsyncSession) -> bool:
    result = await session.execute(select(User).filter(cast(User.telegram_id, BigInteger) == user_id))
    user = result.scalars().first()
    return user is not None


async def update_notifications(user_id: int, value: bool, session: AsyncSession):
    result = await session.execute(
        select(User).filter(User.telegram_id == user_id)
    )
    user = result.scalars().first()
    if user:
        user.notifications = value
        session.add(user)
        await session.commit()


async def get_user(session: Session, telegram_id: int):
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def update_budget(telegram_id: int, new_budget: int, session: AsyncSession):
    stmt = select(User).filter(User.telegram_id == telegram_id)  # Поиск по telegram_id
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise ValueError(f"Пользователь с telegram_id {telegram_id} не найден в базе данных.")

    user.budget = new_budget
    session.add(user)
    await session.commit()
