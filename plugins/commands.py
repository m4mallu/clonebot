import re
import pytz
import asyncio
import datetime
from bot import Bot
from library.sql import *
from presets import Presets
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait
from pyrogram import Client, filters, ContinuePropagation, StopPropagation
from library.chat_support import find_msg_id, find_dc, get_chat_type, get_chat_member_status
from library.buttons import (reply_markup_start, reply_markup_home, reply_markup_close,
                             reply_markup_cap_cnf, reply_markup_terminate)


time_now = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%I:%M:%S %p')
start_date = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).date()


# ----------------------------- Start Message command function --------------------------- #
@Bot.on_message(filters.private & filters.command(['start', 'help']))
async def start(client: Bot, message: Message):
    await message.reply_text(
        Presets.START_TEXT.format(message.from_user.first_name),
        reply_markup=reply_markup_start
    )


# --------------------------------------- Main Window ------------------------------------ #
async def start_options(client: Bot, message: Message):
    await message.reply_text(
        Presets.WELCOME_TEXT,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=reply_markup_home
    )


# ---------------------------------- Text update function -------------------------------- #
@Bot.on_message(filters.private & filters.text | filters.forwarded)
async def text_update_or_terminate(client: Bot, message: Message):
    id = int(message.from_user.id)
    session = await client.USER.get_me()
    regex = r'^%session_start%$'
    if message.forward_from_chat:
        chat_id = int(message.forward_from_chat.id)
        message_id = int(message.forward_from_message_id)
        await message.reply_text(
            Presets.GET_CHAT_ID_MSG.format(chat_id, message_id), reply_markup=reply_markup_close)
        await message.delete()
        raise StopPropagation
    elif message.text and re.search(regex, message.text):
        if message.from_user.id == int(session.id):
            await message.reply_text(Presets.SESSION_START_INFO.format(start_date, time_now),
                                     reply_markup=reply_markup_terminate,
                                     parse_mode=ParseMode.HTML,
                                     protect_content=True,
                                     disable_web_page_preview=True
                                     )
            await message.delete()
            raise StopPropagation
    elif message.text and not message.reply_to_message:
        await message.reply_text(
            text=Presets.TEXT_UPDATE_MSG,
            reply_to_message_id=message.id,
            reply_markup=reply_markup_cap_cnf
        )
    else:
        raise ContinuePropagation


# ------------------------------------ All-n-One Input fn --------------------------------- #
@Client.on_message(filters.private & filters.text & filters.reply)
async def force_reply_msg(client: Bot, message: Message):
    chat_info = message.text
    id = int(message.from_user.id)
    chat_status = []
    member_status = []
    user_bot_me = await client.USER.get_me()
    query = await query_msg(id)
    a = int(query.s_chat_msg_id)
    b = int(query.d_chat_msg_id)
    c = int(query.from_msg_id)
    d = int(query.to_msg_id)
    e = int(query.s_chat)
    f = int(query.d_chat)
    g = int(query.last_msg_id)
    if "https://t.me/joinchat" in message.text:
        chat_info = message.text
    elif "https://t.me/" in message.text:
        chat_info = str(message.text).split('/')[-1]
    elif str(message.text).startswith('-100') and message.text[1:].isdigit():
        chat_info = int(message.text)
    elif ("-100" not in str(message.text)) and str(message.text).isdigit():
        chat_info = int('-100' + str(message.text))
    else:
        pass
    bot_msg = await message.reply_text(Presets.WAIT_MSG)
    if message.reply_to_message_id == a:
        try:
            chat_status = await client.USER.get_chat(chat_info)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            await client.delete_messages(message.chat.id, a)
            await message.delete()
            await bot_msg.edit(Presets.INVALID_CHAT_ID)
            await asyncio.sleep(10)
            await bot_msg.edit_text(Presets.WELCOME_TEXT, reply_markup=reply_markup_home)
            return
        chat_id = int(chat_status.id)
        user_name = chat_status.username
        dc_id = await find_dc(chat_status)
        await asyncio.sleep(1)
        try:
            if chat_id == f:
                await client.delete_messages(message.chat.id, a)
                await message.delete()
                await bot_msg.edit(Presets.CHAT_DUPLICATED_MSG)
                await asyncio.sleep(5)
                await bot_msg.edit_text(Presets.WELCOME_TEXT, reply_markup=reply_markup_home)
                return
        except Exception:
            pass
        await client.delete_messages(message.chat.id, a)
        await message.delete()
        await source_cnf_db(id, chat_id)
        await del_from_to_ids(id)
        clone_btn_count[id] = id
        await bot_msg.edit(Presets.SOURCE_CNF.format(
            chat_status.title,
            chat_id,
            await get_chat_type(chat_status),
            '@' + str(user_name) if bool(user_name) else "𝘗𝘳𝘪𝘷𝘢𝘵𝘦 𝘤𝘩𝘢𝘵",
            dc_id if bool(dc_id) else "𝘊𝘩𝘢𝘵 𝘱𝘩𝘰𝘵𝘰 𝘳𝘦𝘲𝘶𝘪𝘳𝘦𝘥",
            chat_status.members_count),
            reply_markup=reply_markup_close)
        await start_options(client, message)
        await find_msg_id(client, id, chat_id)
    elif message.reply_to_message_id == b:
        await asyncio.sleep(1)
        try:
            chat_status = await client.USER.get_chat(chat_info)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            await bot_msg.edit(Presets.USER_ABSENT_MSG)
            await client.delete_messages(message.chat.id, b)
            await message.delete()
            await asyncio.sleep(10)
            await bot_msg.edit_text(Presets.WELCOME_TEXT, reply_markup=reply_markup_home)
            return
        chat_id = int(chat_status.id)
        user_name = chat_status.username
        dc_id = await find_dc(chat_status)
        try:
            if chat_id == e:
                await client.delete_messages(message.chat.id, b)
                await message.delete()
                await bot_msg.edit(Presets.CHAT_DUPLICATED_MSG)
                await asyncio.sleep(5)
                await bot_msg.edit_text(Presets.WELCOME_TEXT, reply_markup=reply_markup_home)
                return
        except Exception:
            pass
        member = await client.USER.get_chat_member(chat_id, user_bot_me.id)
        if str(await get_chat_type(chat_status)) in ('SUPERGROUP' or 'GROUP'):
            if str(await get_chat_member_status(member)) not in ('ADMINISTRATOR' or 'OWNER'):
                await client.delete_messages(message.chat.id, b)
                await message.delete()
                await bot_msg.edit(Presets.IN_CORRECT_PERMISSIONS_MESSAGE_DEST_POSTING)
                await asyncio.sleep(10)
                await bot_msg.edit_text(Presets.WELCOME_TEXT, reply_markup=reply_markup_home)
                return
            await client.delete_messages(message.chat.id, b)
            await message.delete()
            await target_cnf_db(id, chat_id)
            await bot_msg.edit(Presets.DEST_CNF.format(
                chat_status.title,
                chat_id,
                await get_chat_type(chat_status),
                '@' + str(user_name) if bool(user_name) else "𝘗𝘳𝘪𝘷𝘢𝘵𝘦 𝘤𝘩𝘢𝘵",
                dc_id if bool(dc_id) else "𝘊𝘩𝘢𝘵 𝘱𝘩𝘰𝘵𝘰 𝘳𝘦𝘲𝘶𝘪𝘳𝘦𝘥",
                chat_status.members_count),
                reply_markup=reply_markup_close)
            await asyncio.sleep(2)
            await start_options(client, message)
        else:
            if member.privileges is not None and member.privileges.can_post_messages:
                await client.delete_messages(message.chat.id, b)
                await message.delete()
                await target_cnf_db(id, chat_id)
                await bot_msg.edit(Presets.DEST_CNF.format(
                    chat_status.title,
                    chat_id,
                    await get_chat_type(chat_status),
                    '@' + str(user_name) if bool(user_name) else "𝘗𝘳𝘪𝘷𝘢𝘵𝘦 𝘤𝘩𝘢𝘵",
                    dc_id if bool(dc_id) else "𝘊𝘩𝘢𝘵 𝘱𝘩𝘰𝘵𝘰 𝘳𝘦𝘲𝘶𝘪𝘳𝘦𝘥",
                    chat_status.members_count),
                    reply_markup=reply_markup_close)
                await asyncio.sleep(2)
                await start_options(client, message)
            else:
                await client.delete_messages(message.chat.id, b)
                await message.delete()
                await bot_msg.edit(Presets.IN_CORRECT_PERMISSIONS_MESSAGE_DEST_POSTING)
                await asyncio.sleep(10)
                await bot_msg.edit_text(Presets.WELCOME_TEXT, reply_markup=reply_markup_home)
    elif message.reply_to_message_id == c:
        msg = int()
        if str(message.text).isdigit():
            await asyncio.sleep(1)
            try:
                msg = int(query.last_msg_id)
                if bool(msg) and (int(message.text) > msg):
                    await client.delete_messages(message.chat.id, c)
                    await message.delete()
                    await bot_msg.edit(Presets.OVER_FLOW)
                    await asyncio.sleep(5)
                    await bot_msg.edit_text(Presets.WELCOME_TEXT, reply_markup=reply_markup_home)
                    return
            except Exception:
                pass
            await from_msg_id_cnf_db(id, message.text)
            await client.delete_messages(message.chat.id, c)
            await message.delete()
            await bot_msg.edit(Presets.FROM_MSG_ID_CNF.format(message.text))
            await asyncio.sleep(3)
            await bot_msg.edit_text(Presets.WELCOME_TEXT, reply_markup=reply_markup_home)
        else:
            await client.delete_messages(message.chat.id, c)
            await message.delete()
            await bot_msg.edit_text(Presets.INVALID_MSG_ID)
            await asyncio.sleep(5)
            await bot_msg.edit_text(Presets.WELCOME_TEXT, reply_markup=reply_markup_home)
    elif message.reply_to_message_id == d:
        if str(message.text).isdigit():
            if (g != 0) and int(message.text) > g:
                await client.delete_messages(message.chat.id, d)
                await message.delete()
                await bot_msg.edit(Presets.OVER_FLOW)
                await asyncio.sleep(5)
                await bot_msg.edit_text(Presets.WELCOME_TEXT, reply_markup=reply_markup_home)
                return
            await asyncio.sleep(1)
            await to_msg_id_cnf_db(id, message.text)
            await client.delete_messages(message.chat.id, d)
            await message.delete()
            await bot_msg.edit(Presets.END_MSG_ID_CNF.format(message.text))
            await asyncio.sleep(3)
            await bot_msg.edit_text(Presets.WELCOME_TEXT, reply_markup=reply_markup_home)
        else:
            await client.delete_messages(message.chat.id, d)
            await message.delete()
            await bot_msg.edit_text(Presets.INVALID_MSG_ID)
            await asyncio.sleep(5)
            await bot_msg.edit_text(Presets.WELCOME_TEXT, reply_markup=reply_markup_home)
    else:
        await client.delete_messages(message.chat.id, message.reply_to_message_id)
        await message.delete()
        await bot_msg.edit_text(Presets.INVALID_REPLY_MSG)
        await asyncio.sleep(5)
        await bot_msg.edit_text(Presets.WELCOME_TEXT, reply_markup=reply_markup_home)
