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
            [KeyboardButton(text="⏪ Назад"), KeyboardButton(text="⬅️Предыдущая"), KeyboardButton(text="➡️Следующая")],
        ],
        resize_keyboard=True
    )

def get_cinema_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏪ Назад"), KeyboardButton(text="⬅️Предыдущая"), KeyboardButton(text="➡️Следующая")],
        ],
        resize_keyboard=True
    )

def get_cultural_place_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏪ Назад"), KeyboardButton(text="⬅️Предыдущая"), KeyboardButton(text="➡️Следующая")],
        ],
        resize_keyboard=True
    )

def get_park_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏪ Назад"), KeyboardButton(text="⬅️Предыдущая"), KeyboardButton(text="➡️Следующая")],
        ],
        resize_keyboard=True
    )

def get_recomendation_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍴 Еда"), KeyboardButton(text="🏯 Культурные объекты")],
            [KeyboardButton(text="🎬 Кино"), KeyboardButton(text="🌲Места для прогулки")],
            [KeyboardButton(text="⏪ Назад")],
        ],
        resize_keyboard=True
    )


def get_inline_subscription_keyboard():
    subscribe_button = InlineKeyboardButton(text="Подписаться на рассылку", callback_data="subscribe")
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[subscribe_button]])
    return inline_keyboard


def return_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏪ Назад")],
        ],
        resize_keyboard=True
    )

keyboard_settings = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(text="Изменить кухню", callback_data="edit_cuisine")],
            [InlineKeyboardButton(text="Изменить интересы", callback_data="edit_interests")],
            [InlineKeyboardButton(text="Изменить время", callback_data="edit_time")],
            [InlineKeyboardButton(text="Изменить бюджет", callback_data="edit_budget")],
            [InlineKeyboardButton(text="Изменить уведомления", callback_data="edit_notifications")],
        ],
)

keyboard_cuisine = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Итальянская", callback_data="set_cuisine_italian")],
        [InlineKeyboardButton(text="Японская", callback_data="set_cuisine_japanese")],
        [InlineKeyboardButton(text="Французская", callback_data="set_cuisine_french")]
    ]
)

keyboard_interests = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Путешествия", callback_data="set_interest_travel")],
        [InlineKeyboardButton(text="Технологии", callback_data="set_interest_technology")],
        [InlineKeyboardButton(text="Кулинария", callback_data="set_interest_cooking")]
    ]
)