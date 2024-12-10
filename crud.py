from sqlalchemy.ext.asyncio import AsyncSession
from models import User

async def add_user(user_id: int, username: str, session: AsyncSession):
    # Создаем нового пользователя
    new_user = User(
        telegram_id=user_id,
        username=username,
    )

    session.add(new_user)
    await session.commit()