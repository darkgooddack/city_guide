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
