#----------------------------------- https://github.com/m4mallu/clonebot --------------------------------------------#
import time
import pytz
import datetime
import asyncio
from bot import Bot
from presets import Presets
from plugins.chat_config import start_bot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from init import source_chat, destination_chat, clone_status
from pyrogram.errors import FloodWait
#
bot_start_time = time.time()
#
async def clone_medias(client: Bot, message: Message):
    usr = int(message.chat.id)
    clone_status[usr] = int(message.message_id)
    #
    clone_start_time = time.time()
    current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%I:%M:%S %p')
    #
    doc_files = 0
    video_files = 0
    audio_files = 0
    #
    msg = await client.send_message(
        chat_id=message.chat.id,
        text=Presets.INITIAL_MESSAGE_TEXT,
        disable_notification=True
    )
    msg1 = await client.send_message(
        chat_id=message.chat.id,
        text=Presets.CLOSE_BTN_TXT,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="🌀 CANCEL 🌀", callback_data="stop_clone")]
            ]
        )
    )
    async for user_message in client.USER.iter_history(chat_id=source_chat[usr], reverse=True):
        messages = await client.USER.get_messages(
            source_chat[usr],
            user_message.message_id,
            replies=0,
        )
        time_taken = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - clone_start_time))
        uptime = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - bot_start_time))
        update = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%I:%M:%S %p')
        for file_type in tuple(Presets.FILE_TYPES):
            media = getattr(messages, file_type, None)
            if media is not None:
                if file_type == 'document':
                    doc_files += 1
                elif file_type == 'video':
                    video_files += 1
                elif file_type == 'audio':
                    audio_files += 1
                else:
                    pass
                try:
                    await msg.edit(
                        text=Presets.MESSAGE_COUNT.format(
                            doc_files,
                            video_files,
                            audio_files,
                            time_taken,
                            uptime,
                            current_time,
                            update
                        )
                    )
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                except Exception:
                    pass
                try:
                    await client.USER.copy_message(
                        chat_id=destination_chat[usr],
                        from_chat_id=source_chat[usr],
                        caption=messages.caption,
                        message_id=messages.message_id,
                        disable_notification=True
                    )
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                if usr in clone_status:
                    pass
                else:
                    msg2 = await client.send_message(
                        chat_id=message.chat.id,
                        text=Presets.CANCEL_CLONE
                    )
                    await asyncio.sleep(2)
                    await msg2.edit(
                        text=Presets.CANCELLED_MSG,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(text="HOME", callback_data="home_btn"),
                                 InlineKeyboardButton(text="CLOSE", callback_data="close_btn")]
                            ]
                        )
                    )
                    source_chat.pop(usr)
                    destination_chat.pop(usr)
                    await asyncio.sleep(30)
                    await msg2.delete()
                    return
    #
    await msg1.edit(Presets.FINISHED_TEXT)
    source_chat.pop(usr)
    destination_chat.pop(usr)
    await asyncio.sleep(2)
    await start_bot(client, message)
