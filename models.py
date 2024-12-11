from sqlalchemy import BigInteger
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str] = mapped_column(nullable=True)
    cuisine_preferences: Mapped[str] = mapped_column(nullable=True)
    interests: Mapped[str] = mapped_column(nullable=True)
    available_time: Mapped[str] = mapped_column(nullable=True)
    budget: Mapped[int] = mapped_column(nullable=True)
    notifications: Mapped[bool] = mapped_column(nullable=True)


class FoodPlace(Base):
    __tablename__ = 'food_place'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    address: Mapped[str] = mapped_column(nullable=True)
    link_map: Mapped[str] = mapped_column(nullable=True)
    time: Mapped[str] = mapped_column(nullable=True)
    budget: Mapped[int] = mapped_column(nullable=True)

    food_place_kitchens = relationship("Food_place_Kitchen", back_populates="food_place")


class Food_place_Kitchen(Base):
    __tablename__ = 'food_place_kitchen'

    id: Mapped[int] = mapped_column(primary_key=True)
    food_place_id: Mapped[int] = mapped_column(ForeignKey('food_place.id'), nullable=False)
    kitchen_id: Mapped[int] = mapped_column(ForeignKey('kitchen.id'), nullable=False)

    food_place = relationship("FoodPlace", back_populates="food_place_kitchens")

    kitchen = relationship("Kitchen", back_populates="food_place_kitchens")


class Kitchen(Base):
    __tablename__ = 'kitchen'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)

    food_place_kitchens = relationship("Food_place_Kitchen", back_populates="kitchen")

class Interests(Base):
    __tablename__ = 'interests'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)