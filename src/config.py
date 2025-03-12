"""
Модуль з конфігурацією бота.
"""

import os
from dotenv import load_dotenv
from aiogram import types

# Завантаження змінних середовища
load_dotenv()

# Токен та ім'я бота
BOT_TOKEN = os.getenv("MAIN_BOT_TOKEN")
BOT_NAME = os.getenv("MAIN_BOT_NAME")

# Опис команд бота
COMMANDS = [
    types.BotCommand(command="start", description="Начать работу с ботом"),
        types.BotCommand(command="help", description="Получить помощь"),
]

# Додаємо команди для програм
PROGRAM_COMMANDS = {
    "chrome": "Google Chrome",
    "anydesk": "AnyDesk",
    "telegram": "Telegram",
    "yaware": "YaWare"
}

for program_id, program_name in PROGRAM_COMMANDS.items():
    COMMANDS.append(
        types.BotCommand(
            command=program_id,
                description=f"Установить {program_name}"
        )
    ) 