import pytz
import datetime
from bot import Bot
from presets import Presets
from pyrogram.types import Message
from pyrogram import Client, filters
from library.buttons import reply_markup_terminate


time_now = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%I:%M:%S %p')
start_date = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).date()


@Client.on_message(filters.private & filters.text)
async def text_update(client: Bot, message: Message):
    session = await client.USER.get_me()
    if (message.from_user.id == int(session.id)) and (message.text == "%session_start%"):
        await message.reply_text(Presets.SESSION_START_INFO.format(start_date, time_now),
                                 reply_markup=reply_markup_terminate,
                                 parse_mode='html',
                                 disable_web_page_preview=True
                                 )
    else:
        pass
    await message.delete()
