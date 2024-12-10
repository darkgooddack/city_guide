from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F
import text
import keyboard
from database import get_db
from crud import add_user

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    async for session in get_db():
        await add_user(msg.from_user.id, msg.from_user.username, session)
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=keyboard.get_main_keyboard())


@router.message(F.text == "Меню")
@router.message(F.text == "меню")
async def menu(msg: Message):
    await msg.answer("Выберите один из вариантов:", reply_markup=keyboard.get_main_keyboard())

@router.message(F.text == "✨ Рекомендации")
@router.message(F.text == "⏪Назад")
async def recomendations(msg: Message):
    await msg.answer("Выберите куда вы хотите пойти:", reply_markup=keyboard.get_recomendation_keyboard())

@router.message(F.text == "🍴 Еда")
async def food_place(msg: Message):
    await msg.answer("*список заведений*:", reply_markup=keyboard.get_food_place_keyboard())

@router.message(F.text == "🏯 Культурные объекты")
async def cultural_place(msg: Message):
    await msg.answer("*список заведений*:", reply_markup=keyboard.get_cultural_place_keyboard())

@router.message(F.text == "🎬 Кино")
async def cinema(msg: Message):
    await msg.answer("*список заведений*:", reply_markup=keyboard.get_cinema_keyboard())

@router.message(F.text == "🌲Места для прогулки")
async def park(msg: Message):
    await msg.answer("*список заведений*:", reply_markup=keyboard.get_park_keyboard())

