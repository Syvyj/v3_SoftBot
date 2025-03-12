"""
Ініціалізація модуля src.
"""

from .config import (
    BOT_TOKEN,
    BOT_NAME,
    COMMANDS
)

from .handlers import (
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

from .texts import (
    TEXTS,
    DOWNLOAD_URLS,
    ADMIN_CHAT_ID,
    TRACKER_ADMIN_CHAT_ID
)

from .keyboards import (
    get_main_keyboard,
    get_yaware_keyboard,
    get_help_keyboard,
    get_back_keyboard,
    get_request_keyboard,
    get_download_button,
    get_other_programs_keyboard
)

__all__ = [
    'BOT_TOKEN',
    'BOT_NAME',
    'COMMANDS',
    'cmd_start',
    'cmd_help',
    'handle_main_menu',
    'handle_yaware_menu',
    'handle_help_request',
    'handle_admin_request',
    'handle_other_programs',
    'handle_admin_reply',
    'handle_rating',
    'TEXTS',
    'DOWNLOAD_URLS',
    'ADMIN_CHAT_ID',
    'TRACKER_ADMIN_CHAT_ID',
    'get_main_keyboard',
    'get_yaware_keyboard',
    'get_help_keyboard',
    'get_back_keyboard',
    'get_request_keyboard',
    'get_download_button',
    'get_other_programs_keyboard'
] 