"""
Модуль з обробниками повідомлень бота.
"""

import logging
from pathlib import Path
from aiogram import types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from .texts import (
    TEXTS,
    DOWNLOAD_URLS,
    ADMIN_CHAT_ID,
    TRACKER_ADMIN_CHAT_ID,
    PROGRAM_INFO
)
from .keyboards import (
    get_main_keyboard,
    get_yaware_keyboard,
    get_help_keyboard,
    get_back_keyboard,
    get_request_keyboard,
    get_download_button,
    get_other_programs_keyboard,
    get_rating_keyboard
)
from .faq import find_answer, get_next_ticket_number

# Шляхи до зображень
IMAGES_DIR = Path(__file__).parent.parent / "images"
WELCOME_IMAGE_PATH = IMAGES_DIR / "help_bot.png"
ADMIN_IMAGE_PATH = IMAGES_DIR / "serio.png"
SAD_ROBOT_PATH = IMAGES_DIR / "sad_robot.png"

# Створюємо директорію для зображень, якщо її немає
IMAGES_DIR.mkdir(exist_ok=True)

# Стани FSM
class UserState(StatesGroup):
    WAITING_FOR_PROBLEM = State()
    WAITING_FOR_CONFIRMATION = State()

async def cmd_start(message: types.Message, state: FSMContext):
    """Обробка команди /start"""
    await state.clear()
    
    try:
        # Створюємо об'єкт FSInputFile для локального файлу
        welcome_image = FSInputFile(WELCOME_IMAGE_PATH)
        # Надсилаємо привітання з зображенням
        await message.answer_photo(
            welcome_image,
            caption=TEXTS["welcome"],
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Error in cmd_start: {e}")
        await message.answer(
            TEXTS["welcome"],
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )

async def cmd_help(message: types.Message):
    """Обробка команди /help"""
    await message.answer(
        TEXTS["help"],
        parse_mode="Markdown"
    )

async def handle_main_menu(message: types.Message, state: FSMContext):
    """Обробка головного меню"""
    if message.text == "📥 Установить трекер":
        # Відправляємо перше повідомлення з загальною інформацією
        await message.answer(
            TEXTS["yaware_info"],
            parse_mode="Markdown"
        )
        
        # Відправляємо деталі про роботу трекера
        await message.answer(
            TEXTS["yaware_details"],
            parse_mode="Markdown"
        )
        
        # Створюємо інлайн кнопки для додаткової інформації
        info_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Что такое Yaware?",
                        url="https://yaware.com.ua/uk/what-is-yaware/"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Yaware - программа шпион?",
                        url="https://yaware.com.ua/uk/blog/tajm-treker-ne-shpigunske-programne-zabezpechennya-u-chomu-rizniczya/"
                    )
                ]
            ]
        )
        
        # Відправляємо кнопки для додаткової інформації
        await message.answer(
            "👇 Дополнительная информация:",
            reply_markup=info_keyboard
        )
        
        # Відправляємо фінальне повідомлення з вибором версії
        await message.answer(
            TEXTS["yaware_install"],
            reply_markup=get_yaware_keyboard(),
            parse_mode="Markdown"
        )
    elif message.text == "✅ Я уже установил":
        await message.answer(
            TEXTS["installation_success"],
            reply_markup=get_request_keyboard(),
            parse_mode="Markdown"
        )
    elif message.text == "🔧 Другие программы":
        await message.answer(
            TEXTS["other_programs"],
            reply_markup=get_other_programs_keyboard(),
            parse_mode="Markdown"
        )
    elif message.text == "❓ Нужна помощь админа":
        await state.set_state(UserState.WAITING_FOR_PROBLEM)
        await message.answer(
            TEXTS["help_request"],
            reply_markup=get_back_keyboard()
        )

async def handle_yaware_menu(message: types.Message, state: FSMContext):
    """Обробка меню встановлення YaWare"""
    if message.text == "🪟 Windows":
        await message.answer(
            "🎉 *Отлично!* Ниже по ссылке ты сможешь скачать и установить **YaWare для Windows** ⬇️🪟.\n\n"
            "Также на этой странице есть рекомендации по настройке твоего устройства для работы с трекером 📋🛠️.\n\n"
            "⚠️ Не забывай, что трекер устанавливается на **отдельную рабочую учетную запись** на личном или рабочем устройстве 🖥️🔒.",
            reply_markup=get_download_button(DOWNLOAD_URLS["windows"]),
            parse_mode="Markdown"
        )
    elif message.text == "🍎 MacOS":
        await message.answer(
            "🎉 *Отлично!* Ниже по ссылке ты сможешь скачать и установить **YaWare для MacOS** ⬇️🍏.\n\n"
            "Также на этой странице есть рекомендации по настройке твоего устройства для работы с трекером 📋🛠️.\n\n"
            "⚠️ Не забывай, что трекер устанавливается на **отдельную рабочую учетную запись** на личном или рабочем устройстве 🖥️🔒.",
            reply_markup=get_download_button(DOWNLOAD_URLS["macos"]),
            parse_mode="Markdown"
        )
    elif message.text == "🌐 Плагин":
        await message.answer(
            "🎉 *Отлично!* Ниже по ссылке ты сможешь скачать и установить плагин YaWare для браузера ⬇️🌐.\n\n"
            "Скачайте и установите плагин YaWare для браузера:",
            reply_markup=get_download_button(DOWNLOAD_URLS["plugin"]),
            parse_mode="Markdown"
        )
    elif message.text == "⬅️ Назад":
        await cmd_start(message, state)

async def handle_help_request(message: types.Message, state: FSMContext):
    """Обробка запиту на допомогу"""
    current_state = await state.get_state()
    
    if message.text == "⬅️ Назад":
        await state.clear()
        await cmd_start(message, state)
        return
    
    if message.text == "🔄 Попробовать снова":
        await message.answer(
            "Пожалуйста, опиши свою проблему другими словами:",
            reply_markup=get_back_keyboard()
        )
        return
        
    if current_state == UserState.WAITING_FOR_PROBLEM.state:
        # Зберігаємо повідомлення користувача
        await state.update_data(user_message=message.text)
            
        # Шукаємо відповідь в FAQ
        answer = find_answer(message.text)
        if answer:
            await message.answer(
                answer,
                reply_markup=get_help_keyboard(),
                parse_mode="Markdown"
            )
        else:
            # Відправляємо сумного робота і повідомлення про відсутність рішення
            sad_robot = FSInputFile(SAD_ROBOT_PATH)
            await message.answer_photo(
                sad_robot,
                caption=TEXTS["no_solution"],
                parse_mode="Markdown"
            )
            
            # Пропонуємо звернутися до адміністраторів
            await message.answer(
                "Хочешь обратиться к администраторам за помощью?",
                reply_markup=get_help_keyboard(),
                parse_mode="Markdown"
            )

async def handle_admin_request(message: types.Message, state: FSMContext):
    """Обробка запиту до адміністратора"""
    if message.text == "📨 Отправить запрос":
        username = f"@{message.from_user.username}" if message.from_user.username else f"id{message.from_user.id}"
        user_id = message.from_user.id
        
        try:
            # Створюємо клавіатуру з кнопкою відповіді
            reply_markup = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="↩️ Відповісти",
                        callback_data=f"reply_{user_id}"
                    )]
                ]
            )
            
            # Створюємо об'єкт FSInputFile для зображення
            admin_image = FSInputFile(ADMIN_IMAGE_PATH)
            
            # Відправляємо зображення з текстом адміністраторам
            await message.bot.send_photo(
                TRACKER_ADMIN_CHAT_ID,
                admin_image,
                caption=TEXTS["admin_install_request"].format(username=username),
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
            # Повідомляємо користувача про успіх
            await message.answer(
                TEXTS["request_sent"],
                parse_mode="Markdown"
            )
            
            # Просимо оцінити роботу
            await message.answer(
                TEXTS["rate_request"],
                reply_markup=get_rating_keyboard(),
                parse_mode="Markdown"
            )
        except Exception as e:
            logging.error(f"Failed to send message to admin chat: {e}")
            await message.answer(
                "К сожалению, вышла ошибка при отправке запроса. Пожалуйста, обратитесь к @Oleh_Evrius или @Oleksii_SysAdmin напряму.",
                reply_markup=get_main_keyboard()
            )
        
        await state.clear()
        
    elif message.text == "🔧 Другие программы":
        await message.answer(
            TEXTS["other_programs"],
            reply_markup=get_other_programs_keyboard(),
            parse_mode="Markdown"
        )
        
    elif message.text == "👨‍💻 Обратиться к админу":
        state_data = await state.get_data()
        user_message = state_data.get("user_message", "Не указано")
        username = f"@{message.from_user.username}" if message.from_user.username else f"id{message.from_user.id}"
        user_id = message.from_user.id
        
        try:
            # Створюємо клавіатуру з кнопкою відповіді
            reply_markup = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="↩️ Відповісти",
                        callback_data=f"reply_{user_id}"
                    )]
                ]
            )
            
            # Створюємо об'єкт FSInputFile для зображення
            admin_image = FSInputFile(ADMIN_IMAGE_PATH)
            
            # Відправляємо зображення з текстом адміністраторам
            await message.bot.send_photo(
                ADMIN_CHAT_ID,
                admin_image,
                caption=TEXTS["admin_help_request"].format(
                    ticket_number=get_next_ticket_number(),
                    username=username,
                    user_message=user_message
                ),
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
            # Відправляємо рекомендацію щодо AnyDesk
            anydesk_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="📥 Установить AnyDesk",
                        url=DOWNLOAD_URLS["anydesk"]
                    )]
                ]
            )
            
            await message.answer(
                TEXTS["anydesk_recommendation"],
                reply_markup=anydesk_keyboard,
                parse_mode="Markdown"
            )
            
            # Повідомляємо користувача про успіх
            await message.answer(
                TEXTS["request_sent"],
                parse_mode="Markdown"
            )
            
            # Просимо оцінити роботу
            await message.answer(
                TEXTS["rate_request"],
                reply_markup=get_rating_keyboard(),
                parse_mode="Markdown"
            )
        except Exception as e:
            logging.error(f"Failed to send message to admin chat: {e}")
            await message.answer(
                "К сожалению, вышла ошибка при отправке запроса. Пожалуйста, обратитесь к @Oleh_Evrius или @Oleksii_SysAdmin напряму.",
                reply_markup=get_main_keyboard()
            )
        
        await state.clear()
        
    elif message.text == "⬅️ Назад":
        await state.clear()
        await cmd_start(message, state)

async def handle_other_programs(message: types.Message, state: FSMContext):
    """Обробка меню інших програм"""
    if message.text == "🏠 Главное меню":
        await cmd_start(message, state)
    elif message.text == "❓ Нужна помощь админа":
        await state.set_state(UserState.WAITING_FOR_PROBLEM)
        await message.answer(
            TEXTS["help_request"],
            reply_markup=get_back_keyboard()
        )
    elif message.text in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]:
        program_mapping = {
            "1️⃣": ("chrome", "Google Chrome"),
            "2️⃣": ("anydesk", "AnyDesk"),
            "3️⃣": ("telegram", "Telegram"),
            "4️⃣": ("libreoffice", "LibreOffice"),
            "5️⃣": ("capcut", "CapCut"),
            "6️⃣": ("adspower", "ADSPower")
        }
        
        program_key, program_name = program_mapping[message.text]
        program_url = DOWNLOAD_URLS[program_key]
        program_description = PROGRAM_INFO[program_key]
        
        await message.answer(
            f"*{program_name}*\n\n"
            f"{program_description}\n\n"
            "Нажми кнопку ниже для загрузки:",
            reply_markup=get_download_button(program_url),
            parse_mode="Markdown"
        )

# Додаємо обробник для callback-кнопки відповіді
async def handle_admin_reply(callback: types.CallbackQuery):
    """Обробка натискання кнопки відповіді адміністратором"""
    # Отримуємо ID користувача з callback_data
    user_id = int(callback.data.split('_')[1])
    
    try:
        # Отримуємо інформацію про користувача
        user = await callback.bot.get_chat(user_id)
        username = user.username
        
        if username:
            # Якщо є username, створюємо пряме посилання на чат
            chat_link = f"https://t.me/{username}"
        else:
            # Якщо немає username, використовуємо ID
            chat_link = f"tg://user?id={user_id}"
        
        # Відповідаємо адміністратору з посиланням
        await callback.message.answer(
            f"*Я потурбувався про ваш час, то ж ось кнопка для відповіді користувачу:*\n"
            f"[Відкрити чат]({chat_link})",
            parse_mode="Markdown"
        )
        
        # Відповідаємо на callback
        await callback.answer()
        
    except Exception as e:
        logging.error(f"Error in handle_admin_reply: {e}")
        await callback.answer("Помилка при створенні посилання на чат")

# Додаємо обробник для кнопок оцінки
async def handle_rating(callback: types.CallbackQuery):
    """Обробка оцінки від користувача"""
    try:
        # Отримуємо оцінку з callback_data
        rating = int(callback.data.split('_')[1])
        
        # Дякуємо за оцінку
        await callback.message.answer(
            TEXTS["rating_thanks"],
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
        
        # Видаляємо клавіатуру з оцінками
        await callback.message.edit_reply_markup(reply_markup=None)
        
        # Відповідаємо на callback
        await callback.answer()
        
        # Тут можна додати логіку збереження оцінки в базу даних
        logging.info(f"User {callback.from_user.id} rated the bot with {rating} stars")
        
    except Exception as e:
        logging.error(f"Error in handle_rating: {e}")
        await callback.answer("Помилка при обробці оцінки") 