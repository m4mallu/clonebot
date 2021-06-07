from pyrogram import Client, filters
from library.buttons import reply_markup_terminate
from pyrogram.types import Message
from presets import Presets
from bot import Bot


# -------------------------- Terminate the session if user found it fishy ---------------- #
@Client.on_message(filters.private & filters.command('terminate'))
async def terminate_session(client: Bot, message: Message):
    session = await client.USER.get_me()
    if message.from_user.id == int(session.id):
        await message.reply_text(Presets.PROMPT_TERMINATION,
                                 reply_markup=reply_markup_terminate
                                 )
    else:
        pass
    await message.delete()


