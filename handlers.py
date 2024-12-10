from aiogram import Router, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, \
    KeyboardButton
from aiogram.filters import Command
from aiogram import F
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import update
from sqlalchemy.future import select
import keyboard
from database import get_db
import crud
from database import async_session_factory
from models import FoodPlase, User, Kitchen, Food_place_Kitchen
from urllib.parse import urlparse, parse_qs, unquote



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
                reply_markup=keyboard.get_inline_subscription_keyboard()
            )
        else:
            greeting = f"Привет, {msg.from_user.full_name}! 👋 Мы рады, что вы снова с нами!"

        await msg.answer("Выберите один из вариантов:", reply_markup=keyboard.get_main_keyboard())


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


@router.message(F.text == "🍴 Где поесть")
async def food_place(msg: types.Message):
    async for session in get_db():
        try:
            user_id = msg.from_user.id
            result = await session.execute(
                select(User).where(User.telegram_id == user_id)
            )
            user = result.scalars().first()

            if not user or not user.cuisine_preferences:
                await msg.answer("Мы не знаем ваши предпочтения. Укажите, какая кухня вам нравится!")
                return

            cuisine_preferences = user.cuisine_preferences

            keyboard = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="📍 Отправить геолокацию", request_location=True)]],
                resize_keyboard=True,
                one_time_keyboard=True
            )

            await msg.answer(
                "Пожалуйста, отправьте свою геолокацию, чтобы мы могли подобрать ближайшие заведения.",
                reply_markup=keyboard
            )

        finally:
            await session.close()


@router.message(F.location)
async def handle_location(msg: types.Message):
    async for session in get_db():

        try:
            user_lat = msg.location.latitude
            user_lon = msg.location.longitude

            result = await session.execute(
                select(User).where(User.telegram_id == msg.from_user.id)
            )
            user = result.scalars().first()

            if not user or not user.cuisine_preferences:
                await msg.answer("Мы не знаем ваши предпочтения. Укажите, какая кухня вам нравится!")
                return

            cuisine_preferences = user.cuisine_preferences.split(",")

            restaurants = await get_restaurants(cuisine_preferences, session)

            if not restaurants:
                await msg.answer("К сожалению, мы не нашли подходящих заведений.")
                return

            response = "Мы подобрали для вас следующие заведения:\n\n"
            for restaurant in restaurants[:5]:
                route_url = generate_yandex_maps_route(user_lat, user_lon, restaurant.link_map)
                response += (
                    f"🏠 <b>{restaurant.name}</b>\n"
                    f"📋 {restaurant.description}\n"
                    f"📍 Адрес: {restaurant.address}\n"
                    f"🕒 Время работы: {restaurant.time}\n"
                    f"💵 Средний бюджет: {restaurant.budget} руб.\n"
                    f"🚗 <a href=\"{route_url}\">Построить маршрут</a>\n\n"
                )

            await msg.answer(response, parse_mode="HTML")

        finally:
            await session.close()


#async def get_restaurants(preferences: list[str], session: AsyncSession):
        #    result = await session.execute(
        #select(FoodPlase)
        #.where(FoodPlase.name.in_(preferences))
        #.order_by(FoodPlase.budget.asc())
    #)
    #return result.scalars().all()

async def get_restaurants(preferences: list[str], session: AsyncSession):
    result = await session.execute(
        select(FoodPlase)
        .join(Food_place_Kitchen, FoodPlase.id == Food_place_Kitchen.food_place_id)
        .join(Kitchen, Kitchen.id == Food_place_Kitchen.kitchen_id)
        .where(Kitchen.name.in_(preferences))
        .order_by(FoodPlase.budget.asc())
    )
    return result.scalars().all()

# Function to generate a Yandex Maps route URL
def generate_yandex_maps_route(user_lat: float, user_lon: float, restaurant_link: str):
    parsed_url = urlparse(restaurant_link)
    query_params = parse_qs(parsed_url.query)

    if 'll' in query_params:
        restaurant_coords = query_params['ll'][0]

        restaurant_coords = unquote(restaurant_coords)

        restaurant_lon, restaurant_lat = map(float, restaurant_coords.split(','))

        base_url = "https://yandex.by/maps/?rtext="
        route_url = f"{base_url}{user_lat},{user_lon}~{restaurant_lat},{restaurant_lon}&rtt=auto"
        return route_url
    else:
        return "Ошибка: не удалось извлечь координаты ресторана из ссылки."


@router.message(F.text == "🏯🎭 Интересы")
async def intresting(msg: Message):
    await msg.answer("*список заведений*:", reply_markup=keyboard.get_intresting())

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


def generate_cuisine_keyboard():
    cuisines = ["Японская", "Китайская", "Русская", "Французская"]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=cuisine, callback_data=f"cuisine_{cuisine}")]
            for cuisine in cuisines
        ]
    )
    return keyboard


@router.callback_query(lambda c: c.data == "edit_cuisine")
async def change_cuisine(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Выберите новую кухню:")

    await callback_query.message.edit_reply_markup(reply_markup=generate_cuisine_keyboard())


@router.callback_query(lambda c: c.data.startswith("cuisine_"))
async def save_cuisine(callback_query: CallbackQuery):
    async for session in get_db():
        selected_cuisine = callback_query.data.split("_")[1]

        user_id = callback_query.from_user.id

        stmt = (
            update(User)
            .where(User.telegram_id == user_id)
            .values(cuisine_preferences=selected_cuisine)
        )
        await session.execute(stmt)
        await session.commit()

        await callback_query.message.edit_text(f"Ваши предпочтения обновлены: {selected_cuisine} кухня!")









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
