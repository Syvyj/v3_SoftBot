"""
Модуль з функціями для створення клавіатур.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from .texts import TEXTS

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Створює головну клавіатуру"""
    builder = ReplyKeyboardBuilder()
    
    builder.row(KeyboardButton(text="📥 Установить трекер"))
    builder.row(
        KeyboardButton(text="✅ Я уже установил"),
        KeyboardButton(text="🔧 Другие программы")
    )
    builder.row(KeyboardButton(text="❓ Нужна помощь админа"))
    
    return builder.as_markup(resize_keyboard=True)

def get_yaware_keyboard() -> ReplyKeyboardMarkup:
    """Створює клавіатуру для встановлення YaWare"""
    builder = ReplyKeyboardBuilder()
    
    builder.row(
        KeyboardButton(text="🪟 Windows"),
        KeyboardButton(text="🍎 MacOS"),
        KeyboardButton(text="🌐 Плагин")
    )
    builder.row(
        KeyboardButton(text="✅ Я уже установил"),
        KeyboardButton(text="❓ Нужна помощь админа")
    )
    builder.row(KeyboardButton(text="⬅️ Назад"))
    
    return builder.as_markup(resize_keyboard=True)

def get_help_keyboard() -> ReplyKeyboardMarkup:
    """Створює клавіатуру для меню допомоги"""
    builder = ReplyKeyboardBuilder()
    
    builder.row(KeyboardButton(text="👨‍💻 Обратиться к админу"))
    builder.row(
        KeyboardButton(text="🔄 Попробовать снова"),
        KeyboardButton(text="⬅️ Назад")
    )
    
    return builder.as_markup(resize_keyboard=True)

def get_back_keyboard() -> ReplyKeyboardMarkup:
    """Створює клавіатуру з кнопкою 'Назад'"""
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="⬅️ Назад"))
    return builder.as_markup(resize_keyboard=True)

def get_request_keyboard() -> ReplyKeyboardMarkup:
    """Створює клавіатуру для надсилання запиту"""
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="📨 Отправить запрос")
    )
    builder.row(KeyboardButton(text="⬅️ Назад"),
        KeyboardButton(text="🔧 Другие программы")
        )
    return builder.as_markup(resize_keyboard=True)

def get_download_button(url: str) -> InlineKeyboardMarkup:
    """Створює кнопку для завантаження"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📥 Скачать", url=url)]
        ]
    )
    return keyboard

def get_instruction_keyboard() -> ReplyKeyboardMarkup:
    """Створює клавіатуру для підтвердження встановлення"""
    builder = ReplyKeyboardBuilder()
    
    builder.row(KeyboardButton(text="✅ Я уже установил"))
    builder.row(
        KeyboardButton(text="❓ Нужна помощь админа"),
        KeyboardButton(text="🔄 Начать сначала")
    )
    
    return builder.as_markup(resize_keyboard=True)

def get_final_keyboard() -> ReplyKeyboardMarkup:
    """Створює фінальну клавіатуру"""
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="🔄 Начать сначала"))
    return builder.as_markup(resize_keyboard=True)

def get_rating_keyboard() -> InlineKeyboardMarkup:
    """Створює клавіатуру для оцінки"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⭐", callback_data="rate_1"),
                InlineKeyboardButton(text="⭐⭐", callback_data="rate_2"),
                InlineKeyboardButton(text="⭐⭐⭐", callback_data="rate_3")
            ]
        ]
    )
    return keyboard

def get_other_programs_keyboard() -> ReplyKeyboardMarkup:
    """Створює клавіатуру для меню інших програм"""
    builder = ReplyKeyboardBuilder()
    
    builder.row(
        KeyboardButton(text="1️⃣"),
        KeyboardButton(text="2️⃣"),
        KeyboardButton(text="3️⃣")
    )
    builder.row(
        KeyboardButton(text="4️⃣"),
        KeyboardButton(text="5️⃣"),
        KeyboardButton(text="6️⃣")
    )
    builder.row(
        KeyboardButton(text="🏠 Главное меню"),
        KeyboardButton(text="❓ Нужна помощь админа")
    )
    
    return builder.as_markup(resize_keyboard=True) 