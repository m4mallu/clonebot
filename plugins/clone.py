#----------------------------------- https://github.com/m4mallu/clonebot --------------------------------------------#
import time
import pytz
import asyncio
import datetime
from bot import Bot
from math import trunc
from library.sql import *
from presets import Presets
from pyrogram.types import Message
from library.chat_support import calc_percentage, calc_progress
from library.buttons import reply_markup_stop, reply_markup_finished
from pyrogram.errors import FloodWait
#
bot_start_time = time.time()
#
async def clone_medias(client: Bot, message: Message):
    id = int(message.chat.id)
    query = await query_msg(id)
    cancel_status[id] = int(message.message_id)
    messages = []
    #
    clone_start_time = time.time()
    start_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%I:%M:%S %p')
    uptime = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - bot_start_time))
    #
    file_name = caption = a = b = c = ""
    #
    delay = limit = doc_files = video_files = audio_files = voice_files = photo_files = total_copied = int()
    #
    source_chat = int(query.s_chat)
    target_chat = int(query.d_chat)
    start_id = int(query.from_id)
    end_id = int(query.to_id)
    end_msg_id = int(query.last_msg_id)
    #
    clone_delay = bool(query.delayed_clone)
    default_caption = bool(query.caption)
    fn_caption = bool(query.file_caption)
    #
    if bool(clone_delay) == bool(1):
        delay = 1
    else:
        delay = 0.25
    #
    if start_id > end_id:
        start_id = start_id ^ end_id
        end_id = end_id ^ start_id
        start_id = start_id ^ end_id
    else:
        pass
    #
    if bool(start_id) == bool(0):
        sp = 0
    else:
        sp = start_id
    if bool(end_id) == bool(0):
        ep = end_msg_id
    else:
        ep = end_id
    #
    msg = await message.reply_text(Presets.INITIAL_MESSAGE_TEXT)
    await asyncio.sleep(1)
    msg1 = await message.reply_text(Presets.WAIT_MSG, reply_markup=reply_markup_stop)
    async for user_message in client.USER.iter_history(chat_id=source_chat, reverse=True,
                                                       offset_id=None if bool(start_id) == bool(0) else start_id):
        messages = await client.USER.get_messages(source_chat, user_message.message_id, replies=0)
        message_id = messages.message_id
        if id not in cancel_status:
            msg2 = await message.reply_text(Presets.CANCEL_CLONE)
            await asyncio.sleep(2)
            await msg2.edit(Presets.CANCELLED_MSG, reply_markup=reply_markup_finished)
            await reset_all(id)
            file_types.clear()
            file_types.extend(Presets.FILE_TYPES)
            if int(total_copied) == 0:
                await msg.delete()
            return
        for file_type in file_types:
            media = getattr(messages, file_type, None)
            if media is not None:
                if file_type == 'document':
                    doc_files += 1
                    file_name = messages.document.file_name
                elif file_type == 'video':
                    video_files += 1
                    file_name = messages.video.file_name
                elif file_type == 'audio':
                    audio_files += 1
                    file_name = messages.audio.file_name
                elif file_type == "voice":
                    voice_files += 1
                    file_name = messages.caption
                elif file_type == "photo":
                    photo_files += 1
                    file_name = messages.caption
                else:
                    pass
                if bool(fn_caption) == bool(1):
                    try:
                        caption = str(file_name).rsplit('.', 1)[0]
                    except Exception:
                        file_name = None
                elif bool(default_caption) == bool(1):
                    caption = messages.caption
                else:
                    caption = ""
                total_copied = doc_files + video_files + audio_files + voice_files + photo_files
                pct = await calc_percentage(sp, ep, message_id)
                time_taken = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - clone_start_time))
                update_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%I:%M:%S %p')
                if file_name is not None:
                    if len(file_name) > 64:
                        file_name = None
                    else:
                        a = file_name[:22]
                        b = file_name[22:44]
                        c = file_name[44:]
                try:
                    await msg.edit(
                        Presets.MESSAGE_COUNT.format(
                            a if len(a) > 0 else 11*'➖',
                            b if len(b) > 0 else 13*'➖',
                            c if len(c) > 0 else 13*'➖',
                            "0" if bool(start_id) == bool(0) else start_id,
                            int(messages.message_id),
                            end_msg_id if bool(end_id) == bool(0) else end_id,
                            "✅" if bool(clone_delay) == bool(1) else "❎",
                            "✅" if bool(default_caption) == bool(1) else "❎",
                            "✅" if bool(fn_caption) == bool(1) else "❎",
                            int(total_copied),
                            trunc(pct) if pct <= 100 else "- ",
                            doc_files,
                            video_files,
                            audio_files,
                            photo_files,
                            voice_files,
                            time_taken,
                            uptime,
                            start_time,
                            update_time
                        )
                    )
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                except Exception:
                    pass
                progress = await calc_progress(pct)
                try:
                    await client.USER.copy_message(
                        chat_id=target_chat,
                        from_chat_id=source_chat,
                        caption=caption if bool(caption) == bool(1) else "",
                        message_id=messages.message_id,
                        disable_notification=True
                    )
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                except Exception:
                    await msg1.edit_text(Presets.COPY_ERROR, reply_markup=reply_markup_finished)
                    await reset_all(id)
                    file_types.clear()
                    file_types.extend(Presets.FILE_TYPES)
                    if int(total_copied) == 0:
                        await msg.delete()
                    return
                try:
                    await msg1.edit("🇮🇳 | " + progress if pct <= 100 else Presets.BLOCK, reply_markup=reply_markup_stop)
                except Exception:
                    pass
                await asyncio.sleep(delay)
                if (end_id != bool(0)) and (int(messages.message_id) >= end_id):
                    await reset_all(id)
                    file_types.clear()
                    file_types.extend(Presets.FILE_TYPES)
                    if int(total_copied) == 0:
                        await msg.delete()
                    await msg1.edit(Presets.FINISHED_TEXT, reply_markup=reply_markup_finished)
                    return
                else:
                    pass
    #
    file_types.clear()
    file_types.extend(Presets.FILE_TYPES)
    await reset_all(id)
    if int(total_copied) == 0:
        await msg.delete()
    await msg1.edit(Presets.FINISHED_TEXT, reply_markup=reply_markup_finished)
