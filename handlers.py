from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F
import keyboard
from database import get_db
import crud


router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    async for session in get_db():
        user_exists = await crud.check_user_exists(msg.from_user.id, session)

        if not user_exists:
            await crud.add_user(msg.from_user.id, msg.from_user.username, session)
            await msg.answer(
                text=f"Привет, {msg.from_user.full_name}! 👋 Добро пожаловать в City Guide Ростов-на-Дону! "
                     "📍 Я помогу вам найти лучшие места, маршруты и мероприятия, учитывая ваши интересы, локацию и время. "
                     "🎨 Откройте для себя культурные традиции и уникальные уголки города!",
                reply_markup=keyboard.get_inline_subscription_keyboard()  # Инлайн кнопка подписки
            )


@router.callback_query(lambda c: c.data == "subscribe")
async def subscribe_handler(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    async for session in get_db():
        await crud.update_notifications(user_id, True, session)
        await callback_query.message.answer("Вы успешно подписались на рассылку! 🎉")


@router.message(F.text == "Меню")
@router.message(F.text == "меню")
async def menu(msg: Message):
    await msg.answer("Выберите один из вариантов:", reply_markup=keyboard.get_main_keyboard())

@router.message(F.text == "✨ Рекомендации")
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


@router.message(F.text == "⏪ Назад")
async def park(msg: Message):
    await msg.answer("Вернуться в начало", reply_markup=keyboard.get_main_keyboard())