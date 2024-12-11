from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✨ Рекомендации"), KeyboardButton(text="📢 Мероприятия")],
            [KeyboardButton(text="💸 Скидки и акции"), KeyboardButton(text="⚙️ Настройки")],
        ],
        resize_keyboard=True
    )

def get_recomendation_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍴 Где поесть"), KeyboardButton(text="🎭 Культура")],
            [KeyboardButton(text="🌲 Парки"), KeyboardButton(text="⏪ Назад")],
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

keyboard_interests = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Путешествия", callback_data="set_interest_travel")],
        [InlineKeyboardButton(text="Технологии", callback_data="set_interest_technology")],
        [InlineKeyboardButton(text="Кулинария", callback_data="set_interest_cooking")]
    ]
)