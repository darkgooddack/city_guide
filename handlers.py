import re
from datetime import datetime

import requests
from aiogram import Router, types
from aiogram.client.session import aiohttp
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram import F
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import update
from sqlalchemy.future import select
import keyboard
from database import get_db
import crud
from database import async_session_factory
from models import FoodPlace, User, Kitchen, Food_place_Kitchen
from urllib.parse import urlparse, parse_qs, unquote
from aiogram.fsm.context import FSMContext  # Новый импорт
from aiogram.fsm.state import State,StatesGroup # Новый импорт
from aiogram.filters.state import StateFilter


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

    await msg.answer("Выберите один из вариантов:", reply_markup=keyboard.get_main_keyboard())


async def get_restaurants(preferences: list[str], session: AsyncSession):
    result = await session.execute(
        select(FoodPlace)
        .join(Food_place_Kitchen, FoodPlace.id == Food_place_Kitchen.food_place_id)
        .join(Kitchen, Kitchen.id == Food_place_Kitchen.kitchen_id)
        .where(Kitchen.name.in_(preferences))
        .order_by(FoodPlace.budget.asc())
    )
    return result.scalars().all()

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


async def parse_discounts():
    url = "https://edadeal.ru/journal/tags/aktsii-nedeli/"
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                image_links = []
                rows = soup.find_all("div", class_="row")
                for row in rows:
                    divs = row.find_all("div", class_="col-lg-6")
                    for div in divs:

                        picture = div.find("picture", class_="slick-slide slick-current slick-active")
                        if picture:
                            source = picture.find("source", {"srcset": True})
                            if source:
                                srcset = source.get("srcset", "").split(" ")[0]
                                if srcset:
                                    absolute_url = "https://edadeal.ru" + srcset
                                    image_links.append(absolute_url)

                        additional_source = div.find("source", {"srcset": True})
                        if additional_source:
                            additional_srcset = additional_source.get("srcset", "").split(" ")[0]
                            if additional_srcset and additional_srcset not in image_links:
                                absolute_url = "https://edadeal.ru" + additional_srcset
                                image_links.append(absolute_url)

                return image_links[:5]
            else:
                return []








@router.message(F.text == "💸 Скидки и акции")
async def discounts_handler(msg: Message):
    await msg.answer("Собираю скидки, пожалуйста, подождите...")

    try:
        image_links = await parse_discounts()

        if image_links:
            for link in image_links:
                await msg.answer_photo(photo=link)
        else:
            await msg.answer("К сожалению, скидок пока нет.")
    except Exception as e:
        await msg.answer(f"Произошла ошибка: {e}")

    await msg.answer("Возвращайтесь позже!")


DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"


class Form(StatesGroup):
    waiting_for_date = State()


def get_events(date: str):
    url = f"https://afisha.yandex.ru/rostov-na-donu/selections/nearest-events?date={date}&period=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    events = []
    event_blocks = soup.find_all('div', class_='event events-list__item yandex-sans')

    for event in event_blocks[:5]:  # Берем только первые 5 мероприятий
        img_tag = event.find('img')
        img_url = img_tag['src'] if img_tag else 'Нет изображения'

        link_tag = event.find('a', class_='PlaceLink-fq4hbj-2 fYljjI')
        event_name = link_tag['title'] if link_tag else 'Название не найдено'
        event_link = 'https://afisha.yandex.ru' + link_tag['href'] if link_tag else None

        events.append({
            'name': event_name,
            'link': event_link,
            'img': img_url
        })

    return events


@router.message(lambda message: message.text == "📢 Мероприятия")
async def ask_for_date(msg: Message, state: FSMContext):
    await msg.answer("Пожалуйста, выбери дату мероприятия (например: 2024-12-16).", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.waiting_for_date)  # set_state()

@router.message(StateFilter(Form.waiting_for_date))
async def process_date(msg: Message, state: FSMContext):
    date = msg.text.strip()

    if re.match(DATE_PATTERN, date):
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            await msg.answer("Введите дату в правильном формате (YYYY-MM-DD). Попробуйте еще раз.")
            return

        events = get_events(date)

        if not events:
            await msg.answer("Извините, на эту дату нет мероприятий.")
            await state.clear()
            return

        for event in events[:4]:
            caption = f"{event['name']}\n{event['link'] if event['link'] else 'Ссылка не найдена'}"
            await msg.answer(caption)

            if event['link'] and event['link'] != 'Ссылка не найдена':
                inline_keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="Перейти", url=event['link'])]
                    ]
                )

                await msg.answer(event['img'], reply_markup=inline_keyboard)
            else:

                await msg.answer(event['img'])

        main_keyboard = keyboard.get_main_keyboard()
        await msg.answer("Вот мероприятия на выбранную дату:", reply_markup=main_keyboard)

        await state.clear()

    else:
        await msg.answer("Введите дату в правильном формате (YYYY-MM-DD). Попробуйте еще раз.")







@router.message(F.text == "🎭 Культура")
async def culture(msg: Message):
    await msg.answer("Пока пусто:", reply_markup=keyboard.return_keyboard())


@router.message(F.text == "🌲 Парки")
async def park(msg: Message):
    await msg.answer("Пока пусто:", reply_markup=keyboard.return_keyboard())


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






@router.callback_query(lambda c: c.data == "edit_interests")
async def change_interests(callback_query: CallbackQuery):
    pass

@router.callback_query(lambda c: c.data == "edit_time")
async def change_time(callback_query: CallbackQuery):
    pass





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
