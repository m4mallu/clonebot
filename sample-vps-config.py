import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

class Config(object):

    TG_BOT_TOKEN = ""
    APP_ID = 
    API_HASH = ""
    TG_USER_SESSION = ""
    DB_URI = ""

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
