import copy
import asyncio
from bot import Bot
from library.sql import *
from presets import Presets
from pyrogram.enums import ParseMode
from pyrogram import Client, filters
from library.buttons import types_button
from pyrogram.types import CallbackQuery, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup

opt_type_btns = copy.deepcopy(types_button)
regex_pattern = r'^(docs_yes_btn|docs_no_btn|audio_yes_btn|audio_no_btn|video_yes_btn|video_no_btn' \
                r'|photo_yes_btn|photo_no_btn|voice_yes_btn|voice_no_btn|text_yes_btn|text_no_btn)$'


@Client.on_callback_query(filters.regex(r'^source_btn$'))
async def source_chat_config(client: Bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    await cb.answer(Presets.INFO_CHAT_TYPES, True)
    await cb.message.delete()
    msg = await client.send_message(cb.message.chat.id,
                                    Presets.ASK_SOURCE,
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=ForceReply(True)
                                    )
    s_chat_msg_id = int(msg.id)
    await source_force_reply(id, s_chat_msg_id)
    await asyncio.sleep(30)
    await msg.delete()


@Client.on_callback_query(filters.regex(r'^target_btn$'))
async def target_chat_config(client: Bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    await cb.answer(Presets.INFO_CHAT_TYPES, True)
    await cb.message.delete()
    msg = await client.send_message(cb.message.chat.id,
                                    Presets.ASK_DESTINATION,
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=ForceReply(True)
                                    )
    d_chat_msg_id = int(msg.id)
    await target_force_reply(id, d_chat_msg_id)
    await asyncio.sleep(30)
    await msg.delete()


@Client.on_callback_query(filters.regex(r'^from_btn$'))
async def from_msg_config(client: Bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    ping = await query_msg(id)
    query = int(ping.s_chat)
    if not query:
        await cb.answer(Presets.CNF_SOURCE_FIRST, True)
        return
    await cb.answer(Presets.NOT_REQUIRED)
    await cb.message.delete()
    msg = await client.send_message(cb.message.chat.id,
                                    Presets.ASK_START_MSG_ID,
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=ForceReply(True)
                                    )
    from_msg_id = int(msg.id)
    await from_msg_id_force_reply(id, from_msg_id)
    await asyncio.sleep(30)
    await msg.delete()


@Client.on_callback_query(filters.regex(r'^up_to_btn$'))
async def to_msg_config(client: Bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    ping = await query_msg(id)
    query = int(ping.s_chat)
    if not query:
        await cb.answer(Presets.CNF_SOURCE_FIRST, True)
        return
    await cb.answer(Presets.NOT_REQUIRED)
    await cb.message.delete()
    msg = await client.send_message(cb.message.chat.id,
                                    Presets.ASK_END_MSG_ID,
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=ForceReply(True)
                                    )
    to_msg_id = int(msg.id)
    await to_msg_id_force_reply(id, to_msg_id)
    await asyncio.sleep(30)
    await msg.delete()


@Client.on_callback_query(filters.regex(r'^types_btn$'))
async def set_types(client: Bot, cb: CallbackQuery):
    await cb.answer()
    await cb.message.edit_text(Presets.SELECT_TYPE, reply_markup=InlineKeyboardMarkup(opt_type_btns))


@Client.on_callback_query(filters.regex(regex_pattern))
async def file_types_select(_, cb: CallbackQuery):
    text = Presets.SELECT_TYPE
    if cb.data == "docs_yes_btn":
        await cb.answer()
        file_types.remove("document")
        opt_type_btns[0][0] = InlineKeyboardButton("Docs ❌", callback_data="docs_no_btn")
    elif cb.data == "docs_no_btn":
        await cb.answer()
        file_types.append("document")
        opt_type_btns[0][0] = InlineKeyboardButton("Docs ✅", callback_data="docs_yes_btn")
    elif cb.data == "video_yes_btn":
        await cb.answer()
        file_types.remove("video")
        opt_type_btns[0][1] = InlineKeyboardButton("Video ❌", callback_data="video_no_btn")
    elif cb.data == "video_no_btn":
        await cb.answer()
        file_types.append("video")
        opt_type_btns[0][1] = InlineKeyboardButton("Video ✅", callback_data="video_yes_btn")
    elif cb.data == "audio_yes_btn":
        await cb.answer()
        file_types.remove("audio")
        opt_type_btns[0][2] = InlineKeyboardButton("Audio ❌", callback_data="audio_no_btn")
    elif cb.data == "audio_no_btn":
        await cb.answer()
        file_types.append("audio")
        opt_type_btns[0][2] = InlineKeyboardButton("Audio ✅", callback_data="audio_yes_btn")
    elif cb.data == "photo_yes_btn":
        await cb.answer()
        file_types.remove("photo")
        opt_type_btns[1][0] = InlineKeyboardButton("Photo ❌", callback_data="photo_no_btn")
    elif cb.data == "photo_no_btn":
        await cb.answer()
        file_types.append("photo")
        opt_type_btns[1][0] = InlineKeyboardButton("Photo ✅", callback_data="photo_yes_btn")
    elif cb.data == "voice_yes_btn":
        await cb.answer()
        file_types.remove("voice")
        opt_type_btns[1][1] = InlineKeyboardButton("Voice ❌", callback_data="voice_no_btn")
    elif cb.data == "voice_no_btn":
        await cb.answer()
        file_types.append("voice")
        opt_type_btns[1][1] = InlineKeyboardButton("Voice ✅", callback_data="voice_yes_btn")
    elif cb.data == "text_yes_btn":
        await cb.answer()
        file_types.remove("text")
        opt_type_btns[1][2] = InlineKeyboardButton("Text ❌", callback_data="text_no_btn")
    elif cb.data == "text_no_btn":
        await cb.answer()
        file_types.append("text")
        opt_type_btns[1][2] = InlineKeyboardButton("Text ✅", callback_data="text_yes_btn")
    try:
        await cb.message.edit_text(text, reply_markup=InlineKeyboardMarkup(opt_type_btns))
    except Exception:
        pass


async def update_type_buttons():
    global opt_type_btns
    opt_type_btns.clear()
    opt_type_btns = copy.deepcopy(types_button)
