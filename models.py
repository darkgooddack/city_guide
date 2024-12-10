from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=True)
    cuisine_preferences: Mapped[str] = mapped_column(nullable=True)
    interests: Mapped[str] = mapped_column(nullable=True)
    available_time: Mapped[str] = mapped_column(nullable=True)
    budget: Mapped[int] = mapped_column(nullable=True)