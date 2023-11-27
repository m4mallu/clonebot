#----------------------------------- https://github.com/m4mallu/clonebot --------------------------------------------#
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

class Config(object):

    # Get a bot token from botfather
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "6870054546:AAHpkZ6ElAa13fTB9TysmdU07hE8C3zDAag")

    # Get from my.telegram.org
    APP_ID = int(os.environ.get("APP_ID", "29000421"))

    # Get from my.telegram.org
    API_HASH = os.environ.get("API_HASH", "a5f069cb43b5453f0fd91b80e56fbf4f")

    # Generate a user session string
    TG_USER_SESSION = os.environ.get("TG_USER_SESSION", "BQG6guUAt4_y7fn0Kp27gRgdzVfkABYy95L5UHMLdWXZMJByjw-ufSb8Yl_bQfu9EmDxx07tqGBQRpquPl4iZQVwni3Q_sXiceGJz_Gm7mAQnvbW8kGsU3MEPJK_Vstguu7ag-R-sUoCCOh9x2deadzH-kNMONINrSvi3BaClaRZ-qkz_JGQs3lhW2b6iTwzQ0TgJaulZORonDAMNoQxDi46OnweDes9yBx2ALcI4p-QjmKFQQme1Sppe8El7aqtuNFv-n4v_SCXTZIxHSCk2qVeQsQPulau2vyiwOD0qCC9NaYxP28BinOBw5JqGE2GqxpgkyyUhOdLDPsM_q3d1FPDgqVQwgAAAABfIoKLAA")

    # Database URI
    DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://Anvimitra:suraj8080@atlascluster.fuldnfd.mongodb.net/?retryWrites=true&w=majority")


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
