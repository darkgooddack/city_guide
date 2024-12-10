from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✨ Рекомендации"), KeyboardButton(text="📢 Мероприятия")],
            [KeyboardButton(text="🎉 Новости и тренды"), KeyboardButton(text="⚙️ Настройки")],
        ],
        resize_keyboard=True
    )

def get_settings_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍴 Предпочтения в кухне"), KeyboardButton(text="🎭 Интересы")],
            [KeyboardButton(text="💰 Бюджет"), KeyboardButton(text="⏱️ Доступное время")],
        ],
        resize_keyboard=True
    )

def get_food_place_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏪Назад"), KeyboardButton(text="⬅️Предыдущая"), KeyboardButton(text="➡️Следующая")],
        ],
        resize_keyboard=True
    )

def get_cinema_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏪Назад"), KeyboardButton(text="⬅️Предыдущая"), KeyboardButton(text="➡️Следующая")],
        ],
        resize_keyboard=True
    )

def get_cultural_place_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏪Назад"), KeyboardButton(text="⬅️Предыдущая"), KeyboardButton(text="➡️Следующая")],
        ],
        resize_keyboard=True
    )

def get_park_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏪Назад"), KeyboardButton(text="⬅️Предыдущая"), KeyboardButton(text="➡️Следующая")],
        ],
        resize_keyboard=True
    )

def get_recomendation_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍴 Еда"), KeyboardButton(text="🏯 Культурные объекты")],
            [KeyboardButton(text="🎬 Кино"), KeyboardButton(text="🌲Места для прогулки")],
            [KeyboardButton(text="⏪В меню")],
        ],
        resize_keyboard=True
    )

def get_subscription_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="Подписаться на рассылку"))
    return keyboard
