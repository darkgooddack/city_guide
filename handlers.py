from aiogram import Router, types
from aiogram.fsm.state import StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram import F
import keyboard
from database import get_db
import crud
from database import async_session_factory


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
async def to_the_beginning(msg: Message):
    await msg.answer("Вернуться в начало", reply_markup=keyboard.get_main_keyboard())


@router.message(F.text == "⚙️ Настройки")
async def settings(message: types.Message):
    telegram_id = message.from_user.id


    async for session in get_db():
        user = await crud.get_user(session, telegram_id)

        if not user:
            await message.reply("Пользователь не найден!")
            return

        user_info = (
            f"Ваши данные:\n"
            f"Username: {user.username or 'Не указано'}\n"
            f"Предпочтения в кухне: {user.cuisine_preferences or 'Не указано'}\n"
            f"Интересы: {user.interests or 'Не указано'}\n"
            f"Доступное время: {user.available_time or 'Не указано'}\n"
            f"Бюджет: {user.budget or 'Не указано'}\n"
            f"Уведомления: {'Включены' if user.notifications else 'Отключены'}\n\n"
            f"Хотите что-нибудь изменить?"
        )

        await message.reply(user_info, reply_markup=keyboard.keyboard_settings)


@router.callback_query(lambda c: c.data == "edit_cuisine")
async def change_cuisine(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Выберите новую кухню:")
    await callback_query.message.edit_reply_markup(keyboard.keyboard_cuisine)

# Обработчик на кнопку "Изменить интересы" дописать
@router.callback_query(lambda c: c.data == "edit_interests")
async def change_interests(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Выберите новый интерес:")
    await callback_query.message.edit_reply_markup(keyboard.keyboard_interests)

# Обработчик на кнопку "Изменить время" дописать
@router.callback_query(lambda c: c.data == "edit_time")
async def change_time(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Пожалуйста, укажите доступное время для общения.")


@router.callback_query(lambda c: c.data == "edit_budget")
async def change_budget(callback_query: CallbackQuery):
    keyboard_budget = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1,000 ₽", callback_data="set_budget_1000")],
            [InlineKeyboardButton(text="2,000 ₽", callback_data="set_budget_2000")],
            [InlineKeyboardButton(text="3,000 ₽", callback_data="set_budget_3000")],
            [InlineKeyboardButton(text="5,000 ₽", callback_data="set_budget_5000")],
            [InlineKeyboardButton(text="10,000 ₽", callback_data="set_budget_10000")],
        ]
    )
    await callback_query.message.edit_text(
        "Укажите новый бюджет для ваших предпочтений:",
        reply_markup=keyboard_budget
    )

@router.callback_query(lambda c: c.data.startswith("set_budget_"))
async def set_budget(callback_query: CallbackQuery):
    budget_str = callback_query.data.replace("set_budget_", "")
    try:
        budget = int(budget_str)
    except ValueError:
        await callback_query.answer("Ошибка при выборе бюджета")
        return

    user_id = callback_query.from_user.id

    async with async_session_factory() as session:
        await crud.update_budget(user_id, budget, session)

    await callback_query.answer(f"Бюджет обновлен на {budget} ₽!")

    await send_user_info(callback_query, user_id)


@router.callback_query(lambda c: c.data == "edit_notifications")
async def change_notifications(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    async with async_session_factory() as session:
        user = await crud.get_user(session, user_id)

    if user.notifications:
        keyboard_notifications = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Отключить", callback_data="set_notifications_off")]
            ]
        )
        await callback_query.message.edit_text(
            "Нажимая на кнопку вы отключите уведомления.",
            reply_markup=keyboard_notifications
        )
    else:
        keyboard_notifications = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Включить", callback_data="set_notifications_on")]
            ]
        )
        await callback_query.message.edit_text(
            "Нажимая на кнопку вы включите уведомления.",
            reply_markup=keyboard_notifications
        )


@router.callback_query(lambda c: c.data == "set_notifications_on")
async def set_notifications_on(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    async with async_session_factory() as session:
        await crud.update_notifications(user_id, True, session)

    await callback_query.message.edit_reply_markup(None)

    await send_user_info(callback_query, user_id)


@router.callback_query(lambda c: c.data == "set_notifications_off")
async def set_notifications_off(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    async with async_session_factory() as session:
        await crud.update_notifications(user_id, False, session)

    await callback_query.message.edit_reply_markup(None)

    await send_user_info(callback_query, user_id)


async def send_user_info(callback_query: CallbackQuery, user_id: int):
    async with async_session_factory() as session:
        user = await crud.get_user(session, user_id)

    if not user:
        await callback_query.message.reply("Пользователь не найден!")
        return

    user_info = (
        f"Ваши данные:\n"
        f"Username: {user.username or 'Не указано'}\n"
        f"Предпочтения в кухне: {user.cuisine_preferences or 'Не указано'}\n"
        f"Интересы: {user.interests or 'Не указано'}\n"
        f"Доступное время: {user.available_time or 'Не указано'}\n"
        f"Бюджет: {user.budget or 'Не указано'}\n"
        f"Уведомления: {'Включены' if user.notifications else 'Отключены'}\n\n"
        f"Хотите что-нибудь изменить?"
    )

    await callback_query.message.reply(user_info, reply_markup=keyboard.keyboard_settings)
