from sqlalchemy import cast, BigInteger
from sqlalchemy.ext.asyncio import AsyncSession
from models import User

from sqlalchemy.future import select

async def add_user(user_id: int, username: str, session: AsyncSession):
    # Создаем нового пользователя
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
    # Выполняем запрос для обновления
    result = await session.execute(
        select(User).filter(User.telegram_id == user_id)
    )
    user = result.scalars().first()
    if user:
        user.notifications = value
        session.add(user)
        await session.commit()