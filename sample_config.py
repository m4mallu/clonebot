#----------------------------------- https://github.com/m4mallu/clonebot --------------------------------------------#
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
load_dotenv()

class Config(object):

    # Get a bot token from botfather
    TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "")

    # Get from my.telegram.org
    APP_ID = int(os.getenv("APP_ID", ""))

    # Get from my.telegram.org
    API_HASH = os.getenv("API_HASH", "")

    # Generate a user session string
    TG_USER_SESSION = os.getenv("TG_USER_SESSION", "")

    # Database URI
    DB_URI = os.getenv("DATABASE_URL", "")


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
