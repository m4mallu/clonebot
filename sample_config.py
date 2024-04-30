#----------------------------------- https://github.com/m4mallu/clonebot --------------------------------------------#
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

class Config(object):

    # Get a bot token from botfather
    TG_BOT_TOKEN = "Your_Telegram_bot_token"

    # Get from my.telegram.org
    APP_ID = int(Your_telegram_App_Id)

    # Get from my.telegram.org
    API_HASH = "Your_Telegram_Api_Hash"

    # Generate a user session string
    TG_USER_SESSION = "Your_user_session_string_compatible_with_Pyrogram_v2"

    # Database URI
    DB_URI = "Your_database_URI"


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
