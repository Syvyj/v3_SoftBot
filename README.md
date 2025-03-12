

# Telegram Bot Helper

A Telegram bot designed to help with software installation and support.

## Features

- YaWare tracker installation assistance
- Step-by-step instructions
- FAQ and support
- Admin communication
- Multi-program installation support

## Requirements

- Python 3.8 or higher
- Internet connection
- Telegram Bot Token

## Installation

### Windows

1. Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. Clone or download this repository
3. Open Command Prompt in the project directory
4. Run the setup script:
   ```cmd
   python setup.py
   ```

### macOS/Linux

1. Install Python 3.8+ if not installed:
   - macOS (with Homebrew):
     ```bash
     brew install python
     ```
   - Ubuntu/Debian:
     ```bash
     sudo apt update
     sudo apt install python3 python3-venv
     ```
2. Clone or download this repository
3. Open Terminal in the project directory
4. Run the setup script:
   ```bash
   python3 setup.py
   ```

## Configuration

1. Get a Telegram Bot Token from [@BotFather](https://t.me/BotFather)
2. Edit the `.env` file in the project directory:
   ```
   BOT_TOKEN=your_bot_token_here
   ADMIN_CHAT_ID=your_admin_chat_id_here
   TRACKER_ADMIN_CHAT_ID=your_tracker_admin_chat_id_here
   ```

## Running the Bot

### Windows
```cmd
.venv\Scripts\python bot.py
```

### macOS/Linux
```bash
.venv/bin/python bot.py
```

## Project Structure

```
.
├── bot.py              # Main bot file
├── setup.py           # Setup script
├── requirements.txt   # Python dependencies
├── .env              # Environment variables
├── README.md         # This file
├── src/              # Source code
│   ├── __init__.py
│   ├── handlers.py   # Message handlers
│   ├── keyboards.py  # Keyboard layouts
│   ├── texts.py      # Bot messages
│   └── faq.py        # FAQ system
├── data/             # Data storage
└── images/           # Bot images
```

## Troubleshooting

### Windows
- If you get "python not found", make sure Python is added to PATH during installation
- Run Command Prompt as Administrator if you encounter permission errors

### macOS
- If you get "command not found: python3", install Python using Homebrew
- Make sure you have full disk access for Terminal in System Preferences

### Linux
- Install python3-venv if you get virtual environment errors:
  ```bash
  sudo apt install python3-venv
  ```
- Make sure you have write permissions in the project directory

## Support

If you encounter any issues:
1. Check the Troubleshooting section
2. Make sure all requirements are installed
3. Verify your .env configuration
4. Contact the administrator through the bot

## License

This project is proprietary software. All rights reserved.

## Основні можливості

- Вибір операційної системи (Windows/MacOS)
- Вибір програми для встановлення
- Отримання посилань на завантаження
- Звернення до системного адміністратора

## Налаштування

1. Встановіть необхідні залежності:
```bash
pip install -r requirements.txt
```

2. Налаштуйте токен бота:
   - Отримайте токен у [@BotFather](https://t.me/BotFather)
   - Встановіть змінну середовища:
     ```bash
     export BOT_TOKEN='your_bot_token_here'
     ```
   - Або створіть файл `.env` з вмістом:
     ```
     BOT_TOKEN=your_bot_token_here
     ```

## Запуск бота

```bash
python bot.py
```

## Як модифікувати бота

### 1. Додавання нової програми

- Додайте опис програми в `TEXTS["programs"]`:
```python
"programs": {
    "new_program": "🆕 New Program\n\nОпис нової програми."
}
```

- Додайте URL для завантаження в `DOWNLOAD_URLS`:
```python
"new_program": {
    "windows": "https://download.link/windows",
    "mac": "https://download.link/mac"
}
```

- Додайте кнопку в функції `get_programs_keyboard()`
- За потреби, додайте нову команду в список `COMMANDS`

### 2. Зміна текстів

Всі тексти знаходяться в словнику `TEXTS`. Кожен текст має свій ключ:
- `welcome` - привітальне повідомлення
- `programs_list` - список програм
- `support_text` - текст для звернення до адміністратора
- та інші

### 3. Додавання нових кнопок

Клавіатури створюються в трьох функціях:
- `get_os_keyboard()` - клавіатура вибору ОС
- `get_programs_keyboard()` - клавіатура з програмами
- `get_navigation_keyboard()` - навігаційна клавіатура

### 4. Зміна логіки роботи

Основні обробники команд та кнопок знаходяться в функціях з декоратором `@dp.message`. Кожна функція має детальний опис своєї роботи в коментарях.

## Доступні команди

- `/start` - Запустити бота
- `/help` - Показати доступні команди
- `/chrome` - Інформація про встановлення Google Chrome
- `/anydesk` - Інформація про встановлення AnyDesk
- `/telegram` - Інформація про встановлення Telegram
- `/yaware` - Інформація про встановлення YaWare 
