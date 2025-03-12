"""
Telegram бот для допомоги з встановленням програмного забезпечення.
Основні можливості:
- Встановлення трекера YaWare
- Покрокові інструкції
- Відповіді на питання
- Звʼязок з адміністратором
"""

import asyncio
import logging
import signal
import sys
from pathlib import Path
from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage

from src import (
    BOT_TOKEN,
    COMMANDS,
    cmd_start,
    cmd_help,
    handle_main_menu,
    handle_yaware_menu,
    handle_help_request,
    handle_admin_request,
    handle_other_programs,
    handle_admin_reply,
    handle_rating
)

# Налаштування логування
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            Path('data/support_bot.log').absolute(),
            encoding='utf-8'
        )
    ]
)
logger = logging.getLogger(__name__)

# Ensure required directories exist
Path('data').mkdir(exist_ok=True)
Path('images').mkdir(exist_ok=True)

# Ініціалізація бота та диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Реєстрація обробників команд
dp.message.register(cmd_start, Command("start"))
dp.message.register(cmd_help, Command("help"))

# Реєстрація обробників повідомлень
dp.message.register(handle_main_menu, lambda message: message.text in [
    "📥 Установить трекер",
    "✅ Я уже установил",
    "🔧 Другие программы",
    "❓ Нужна помощь админа"
])

dp.message.register(handle_yaware_menu, lambda message: message.text in [
    "🪟 Windows",
    "🍎 MacOS",
    "🌐 Плагин",
    "❓ Нужна помощь админа",
    "✅ Я уже установил",
    "⬅️ Назад"
])

dp.message.register(handle_other_programs, lambda message: message.text in [
    "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣",
    "🏠 Главное меню",
    "❓ Нужна помощь админа"
])

dp.message.register(handle_admin_request, lambda message: message.text in [
    "📨 Отправить запрос",
    "👨‍💻 Обратиться к админу",
    "🔧 Другие программы",
    "⬅️ Назад"
])

# Реєстрація обробника callback-кнопки відповіді
dp.callback_query.register(handle_admin_reply, F.data.startswith("reply_"))

# Реєстрація обробника callback-кнопок оцінки
dp.callback_query.register(handle_rating, F.data.startswith("rate_"))

# Всі інші повідомлення обробляються як запити на допомогу
dp.message.register(handle_help_request)

async def on_startup():
    """Дії при запуску бота"""
    try:
        # Встановлюємо команди бота
        await bot.set_my_commands(COMMANDS)
        # Перевіряємо, що команди встановлені
        bot_commands = await bot.get_my_commands()
        if not bot_commands:
            logger.warning("Commands were not set properly!")
        else:
            logger.info(f"Bot started with {len(bot_commands)} commands")
    except Exception as e:
        logger.error(f"Error setting commands: {e}")

async def on_shutdown():
    """Дії при зупинці бота"""
    logger.info("Shutting down...")
    try:
        await bot.session.close()
        logger.info("Bot session closed")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
    finally:
        logger.info("Bye!")

def handle_signals():
    """Обробка сигналів завершення"""
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            sig,
            lambda s=sig: asyncio.create_task(shutdown(sig=s))
        )

async def shutdown(sig: signal.Signals):
    """Graceful shutdown"""
    logger.info(f'Received signal {sig.name}...')
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    logger.info(f'Cancelling {len(tasks)} outstanding tasks')
    await asyncio.gather(*tasks, return_exceptions=True)
    await on_shutdown()
    loop = asyncio.get_event_loop()
    loop.stop()

async def main():
    """Головна функція"""
    try:
        logger.info("Starting bot...")
        handle_signals()
        await on_startup()
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        await on_shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (KeyboardInterrupt)")
    except Exception as e:
        logger.error(f"Bot stopped due to error: {e}")
    finally:
        sys.exit(0) 