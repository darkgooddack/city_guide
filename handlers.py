from aiogram import Router
from aiogram.types import Message, CallbackQuery, InputFile
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
        image_path = "static/welcome_image.jpg"
        photo = InputFile(image_path)

        await msg.answer_photo(
            photo=photo,
            caption=text.greet.format(name=msg.from_user.full_name),
            reply_markup=get_subscription_keyboard()  # Кнопка "Подписаться на рассылку"
        )

@router.message(F.text == "Меню")
@router.message(F.text == "меню")
async def menu(msg: Message):
    await msg.answer("Выберите один из вариантов:", reply_markup=keyboard.get_main_keyboard())