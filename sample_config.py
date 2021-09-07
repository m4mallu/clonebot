#----------------------------------- https://github.com/m4mallu/clonebot --------------------------------------------#
import os
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            "clonebot-ui.txt",
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

class Config(object):

    # Get a bot token from botfather
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "1958860703:AAGnjV2cT39iqimI7U8ud6eimkMnOf4adtk")

    # Get from my.telegram.org
    APP_ID = int(os.environ.get("APP_ID", "7880410"))

    # Get from my.telegram.org
    API_HASH = os.environ.get("API_HASH", "72fb94902bbee2b74318b3d499c1096e")

    # Authorized users to use this bot
    AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "1162457830").split())

    # Generate a user session string
    TG_USER_SESSION = os.environ.get("TG_USER_SESSION", "BQDAJa38FX2U-cRxWdvDxKr8NHResf_Mhx7XK2WESIgpGFcf7g9nXMgx_XTiNza_CAL2qbLRir_it2u-Nv9Uoz9QE47W7EG73MC9cNiOzYOk14R0fdDcgalag_cCX534ST7GJHZiag7LadfogjDvukE-U797f3d9gXHsypnta-n5szVUEjJnPYzUvbH1Ml7m2-CkHmGrmL07E1GrUyTAv9oEzXS9zf-V2Orqu-m-8D0vxNkoqn0t_H-0cJG0MDAsY0eRbc5aBp_aUa8ILn-S6278WYN30wlf0rK6ZE07E7RFsxsuG2PZ7qQre1-uWR6vnEJ4HT13OteVHx7JY84S1ZioafEatwA")

    # Database URI
    DB_URI = os.environ.get("DATABASE_URL", "postgres://yfwoikoxtqxoef:2771e4fb3b9f3c78854e4212d7af1facab1f9a0b383d3b1bc2354f5925bf9d71@ec2-34-192-72-159.compute-1.amazonaws.com:5432/da2hdqej884g6v")


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
